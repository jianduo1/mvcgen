from tortoise.models import Model as TortoiseModel, ModelMeta as TortoiseModelMeta
from tortoise.queryset import QuerySet, QuerySetSingle, Prefetch
from tortoise.fields import relational
from tortoise.transactions import atomic
from fastapi import APIRouter, HTTPException, Query
from typing import Dict, Any, Optional, List, Type
from .schemas import Meta, Schema, SchemaMeta
from pydantic import BaseModel as PydanticModel
import json


class ModelMeta(TortoiseModelMeta):
    def __new__(cls, name, bases, attrs):
        update_attrs = {}
        for attr in attrs.values():
            if isinstance(attr, Meta):

                class Meta_:
                    table = attr.table
                    table_description = attr.table_desc

                update_attrs["Meta"] = Meta_
        attrs.update(update_attrs)
        return super().__new__(cls, name, bases, attrs)


class Model(TortoiseModel, metaclass=ModelMeta):
    id = None  # 由子类定义
    response_schema: PydanticModel = None
    create_schema: PydanticModel = None
    update_schema: PydanticModel = None

    class Meta:
        abstract = True

    @classmethod
    @atomic()
    async def create(cls, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """创建记录"""
        relations = cls._extract_relations(data)
        instance = await super().create(**data)
        await cls._handle_relations(instance, relations)
        return await cls._format_response(instance)

    @classmethod
    async def get(cls, id: int) -> Optional[Dict[str, Any]]:
        """获取单条记录"""
        query: QuerySetSingle[TortoiseModel] = super().get(id=id)
        query = query.prefetch_related(*cls._meta.fetch_fields)
        instance: TortoiseModel = await query
        return await cls._format_response(instance)

    @classmethod
    async def get_all(
        cls,
        filters: Optional[Dict[str, Any]] = None,
        order_by: Optional[List[str]] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> List[Any]:
        """获取所有记录"""
        queryset: QuerySet = cls.all()
        o2o_fields = []
        prefetch_fields = []
        for field_name in cls._meta.fetch_fields:
            field = cls._meta.fields_map.get(field_name)
            if not field:
                prefetch_fields.append(field_name)
                continue
            if isinstance(field, relational.OneToOneFieldInstance):
                o2o_fields.append(field_name)
            elif cls._is_self_referencing_field(field_name):
                prefetch_fields.append(Prefetch(field_name, queryset=cls.all().prefetch_related(field_name)))
            else:
                prefetch_fields.append(field_name)
        if o2o_fields:
            queryset = queryset.select_related(*o2o_fields)
        if prefetch_fields:
            queryset = queryset.prefetch_related(*prefetch_fields)
        if filters:
            queryset = queryset.filter(**filters)
        if order_by:
            queryset = queryset.order_by(*order_by)
        if offset:
            queryset = queryset.offset(offset)
        if limit:
            queryset = queryset.limit(limit)
        return [await cls._format_response(instance) for instance in await queryset]

    @classmethod
    async def _format_response(cls, instance: TortoiseModel) -> Dict[str, Any]:
        """格式化响应数据"""
        common_fields = cls._meta.fields - cls._meta.fetch_fields
        instance_data = {}
        for field in common_fields:
            instance_data[field] = getattr(instance, field)
        for key, value in instance.__dict__.items():
            if isinstance(value, relational.BackwardFKRelation):
                field_name = key[1:]
                related_objects = value.__dict__["related_objects"]
                instance_data[field_name] = [{k: v for k, v in obj.__dict__.items() if not k.startswith("_")} for obj in related_objects]
            elif isinstance(value, TortoiseModel):
                field_name = key[1:]
                if isinstance(value, list):
                    instance_data[field_name] = [{k: v for k, v in obj.__dict__.items() if not k.startswith("_")} for obj in value]
                else:
                    instance_data[field_name] = {k: v for k, v in value.__dict__.items() if not k.startswith("_")}
            elif key[1:] in cls._meta.fetch_fields and value is None:
                field_name = key[1:]
                instance_data[field_name] = None
        return instance_data

    @classmethod
    @atomic()
    async def update(cls, id: int, data: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """更新记录"""
        instance = await cls.get(id=id)
        relations = cls._extract_relations(data)
        await instance.update_from_dict(data).save()
        await cls._handle_relations(instance, relations)
        return await cls._format_response(instance)

    @classmethod
    @atomic()
    async def delete(cls, id: int) -> bool:
        """删除记录"""
        try:
            instance = await cls.get(id=id)
            await instance.delete()
            return True
        except:
            return False

    @classmethod
    @atomic()
    async def batch_create(cls, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """批量创建"""
        results = []
        for data in data_list:
            result = await super().create(data)
            if result:
                results.append(result)
        return results

    @classmethod
    @atomic()
    async def batch_update(cls, data_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """批量更新"""
        results = []
        for data in data_list:
            if "id" not in data:
                continue
            result = await cls.update(data["id"], data)
            if result:
                results.append(result)
        return results

    @classmethod
    @atomic()
    async def batch_delete(cls, ids: List[int]) -> int:
        """批量删除"""
        return await cls.filter(id__in=ids).delete()

    @classmethod
    def _is_self_referencing_field(cls, field_name: str) -> bool:
        """检查字段是否是自引用字段"""
        field = cls._meta.fields_map.get(field_name)
        return field and isinstance(field, relational.ForeignKeyFieldInstance) and field.related_model == cls

    @classmethod
    def _extract_relations(cls, data: Dict[str, Any]) -> Dict[str, Any]:
        """提取关联数据"""
        relations = {k: data.pop(k) for k in cls._meta.fetch_fields if k in data}
        return relations

    @classmethod
    async def _handle_relations(cls, instance: TortoiseModel, relations: Dict[str, Any]) -> None:
        """创建关联关系记录"""
        for field_name, value in relations.items():
            field = cls._meta.fields_map[field_name]
            if isinstance(field, relational.ManyToManyFieldInstance):
                if value and isinstance(value, list) and len(value) > 0:
                    if all(isinstance(item, int) for item in value):
                        related_objects = await super(Model, field.related_model).filter(id__in=value)
                    elif all(isinstance(item, dict) for item in value):
                        related_objects = [await super(Model, field.related_model).create(**item) for item in value]
                    else:
                        raise ValueError(f"Invalid value type for field {field_name}: {type(value)}")
                    await getattr(instance, field_name).add(*related_objects)
            elif isinstance(field, relational.ForeignKeyFieldInstance):
                if value is None:
                    setattr(instance, field_name, None)
                elif isinstance(value, dict):
                    related_objects = await super(Model, field.related_model).create(**value)
                elif isinstance(value, int):
                    related_objects = await super(Model, field.related_model).get(id=value)
                else:
                    raise ValueError(f"Invalid value type for field {field_name}: {type(value)}")
                if value is not None:
                    setattr(instance, field_name, related_objects)
                await instance.save()

    @classmethod
    def get_fields(cls) -> Dict[str, List[str]]:
        """获取模型所有字段"""
        backward_fields = cls._meta.backward_fk_fields | cls._meta.backward_o2o_fields
        forward_fields = cls._meta.fetch_fields - backward_fields
        common_fields = cls._meta.fields - cls._meta.fetch_fields
        return {"common_fields": common_fields, "forward_fields": forward_fields, "backward_fields": backward_fields}

    def __init_subclass__(cls, **kwargs):
        update_attrs = {}
        for attr in cls.__dict__.values():
            if isinstance(attr, Schema):

                class Schema_(PydanticModel, metaclass=SchemaMeta):
                    __model__ = cls
                    __fields__ = attr.fields
                    __is_exclude__ = attr.is_exclude

                update_attrs[f"{attr.model}_schema"] = Schema_
        for k, v in update_attrs.items():
            setattr(cls, k, v)

    @classmethod
    def get_router(cls, prefix: str, tags: List[str]):
        """获取路由"""
        router = APIRouter(prefix=prefix, tags=tags)

        @router.post("/", response_model=cls.response_schema)
        async def create(request: cls.create_schema):
            result = await cls.create(request.model_dump())
            if not result:
                raise HTTPException(status_code=400, detail="创建失败")
            return result

        @router.get("/{id}", response_model=cls.response_schema)
        async def get(id: int):
            data = await cls.get(id=id)
            if not data:
                raise HTTPException(status_code=404, detail="记录不存在")
            return data

        @router.get("/", response_model=List[cls.response_schema])
        async def get_all(
            order_by: List[str] = Query(None, description="排序字段，列表形式，例如 ['-created_at', 'name']"),
            filters: str = Query(None, description='过滤条件，字典形式，例如 {"name": "John"}'),
            offset: int = Query(None, description="跳过记录数"),
            limit: int = Query(None, description="返回记录数"),
        ):
            filters_dict = None
            if filters:
                try:
                    filters_dict = json.loads(filters)
                except json.JSONDecodeError:
                    raise HTTPException(status_code=400, detail="filters 参数必须是有效的 JSON 字符串")
            return await cls.get_all(order_by=order_by, filters=filters_dict, offset=offset, limit=limit)

        @router.put("/{id}", response_model=cls.response_schema)
        async def update(id: int, request: cls.update_schema):
            data = await cls.update(id, request.model_dump(exclude_unset=True))
            if not data:
                raise HTTPException(status_code=404, detail="记录不存在")
            return data

        @router.delete("/{id}")
        async def delete(id: int, cascade: bool = Query(False, description="是否级联删除")) -> dict:
            result = await cls.delete(id, cascade=cascade)
            if not result:
                raise HTTPException(status_code=404, detail="记录不存在")
            return {"success": True, "message": "删除成功"}

        @router.post("/batch_create", response_model=List[cls.response_schema])
        async def batch_create(requests: List[cls.create_schema]):
            return await cls.batch_create([r.model_dump() for r in requests])

        @router.put("/batch_update", response_model=List[cls.response_schema])
        async def batch_update(requests: List[cls.update_schema]):
            return await cls.batch_update([r.model_dump() for r in requests])

        @router.delete("/batch_delete")
        async def batch_delete(ids: List[int]) -> dict:
            result = await cls.batch_delete(ids)
            return {"success": True, "deleted_count": result}

        return router
