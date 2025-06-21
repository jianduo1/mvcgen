from tortoise import fields

def Int(desc, default=None):
    """整数字段"""
    return fields.IntField(desc=desc, default=default, null=True, blank=True)

def Char(max_length, desc, default=''):
    """字符串字段"""
    return fields.CharField(max_length=max_length, desc=desc, default=default, null=True, blank=True)

def Text(desc, default=''):
    """文本字段"""
    return fields.TextField(desc=desc, default=default, null=True, blank=True)

def Json(desc, default=dict):
    """JSON字段"""
    return fields.JSONField(desc=desc, default=default, null=True, blank=True)

def Datetime(desc, default=None):
    """日期时间字段"""
    return fields.DatetimeField(desc=desc, default=default, null=True, blank=True)

def FK(model_dot_field, desc, default=None):
    """单向外键关系"""
    model_name, related_name = model_dot_field.split(".")
    model_name = "models." + model_name
    return fields.ForeignKeyField(model_name=model_name, related_name=related_name, description=desc, default=default, null=True, blank=True)

def M2M(model_dot_field, table, desc, default=None):
    """多对多关系"""
    model_name, related_name = model_dot_field.split(".")
    model_name = "models." + model_name
    return fields.ManyToManyField(model_name=model_name, related_name=related_name, through=table, description=desc, default=default) 