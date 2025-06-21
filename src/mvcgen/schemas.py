"""
模式定义模块，提供动态生成 Pydantic 模型的功能。
"""

from typing import Dict, Any, List, Optional, Type, Literal
from pydantic import BaseModel as PydanticModel, Field as PydanticField
from tortoise.models import Model as TortoiseModel
from dataclasses import dataclass


class SchemaMeta(type(PydanticModel)):
    """动态生成Schema的元类，集成模型信息提取逻辑"""

    def __new__(cls, name, bases, namespace):
        # 获取模型配置
        model: Optional[Type[TortoiseModel]] = namespace.get("__model__")
        if not model:
            return super().__new__(cls, name, bases, namespace)

        fields = namespace.get("__fields__", [])  # 包含字段
        is_exclude = namespace.get("__is_exclude__", False)  # 是否排除字段
        related_fields_ = namespace.get("__related_fields__", lambda x: {})  # 关联字段

        # 获取所有字段
        all_fields = model._meta.fields_map
        if is_exclude:
            fields = [f for f in all_fields if f not in fields]
        else:
            fields = [f for f in fields if f in all_fields]
        if isinstance(fields, list):
            fields = {f: f for f in fields}

        # 映射字段类型，从 tortoise 映射到 pydantic
        type_map = {
            # 普通字段
            "IntField": int,
            "CharField": str,
            "TextField": str,
            "JSONField": Dict | List,
            "BooleanField": bool,
            "FloatField": float,
            "DatetimeField": str,
            # 关联字段
            "OneToOneFieldInstance": Dict | int,
            "ForeignKeyFieldInstance": Dict | int,
            "BackwardOneToOneRelation": Dict | int,
            "BackwardFKRelation": List[Dict | int],
            "ManyToManyFieldInstance": List[Dict | int],
        }

        new_namespace = {"__annotations__": {}}

        for field_name in fields:
            field: fields.Field = all_fields[field_name]

            # 构建字段类型，如果字段为空，则类型为可选类型
            _type = type_map[type(field).__name__]
            # 处理_id结尾的关联字段类型：只能是int，表示已存在的对象
            if field.source_field == field.model_field_name:
                _type = int
            # 处理关联字段：处理一对一，正向一对多关联字段默认值：类型为dict，表示新创建的对象，或者类型为int，表示已存在的对象
            elif isinstance(field, fields.relational.RelationalField):
                if isinstance(field, (fields.relational.OneToOneFieldInstance, fields.relational.ForeignKeyFieldInstance, fields.relational.BackwardOneToOneRelation)):
                    field.default = None
                # 处理反向一对多，多对多关联字段默认值：类型为list，表示新创建的对象，或者类型为int，表示已存在的对象
                elif isinstance(field, (fields.relational.BackwardFKRelation, fields.relational.ManyToManyFieldInstance)):
                    field.default = []

            # 设置字段类型和可选性
            field_type = Optional[_type] if field.null else _type

            # 构建Pydantic字段校验对象
            field_obj = PydanticField(
                default=field.default,
                description=field.description,
                nullable=field.null or field.required,
                alias=fields[field_name],
            )

            # 创建Pydantic模型的命名空间，注入字段类型标注和字段对象
            new_namespace["__annotations__"][field_name] = field_type
            new_namespace[field_name] = field_obj

        return super().__new__(cls, name, bases, new_namespace)


class Schema:
    """
    响应模型配置
    """

    def __init__(self, model: Literal["create", "update", "response"], fields: List[str], is_exclude: bool = False):
        self.model = model
        self.fields = fields
        self.is_exclude = is_exclude 


@dataclass
class Meta:
    """模型配置元信息"""

    table: str
    table_desc: str
