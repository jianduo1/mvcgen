# API 参考

## Agent 类

主要的代码生成智能体类。

### 初始化

```python
from mvcgen import Agent

agent = Agent(
    model_name="gpt-4",
    temperature=0.7,
    max_tokens=2000
)
```

### 方法

#### `run(prompt: str) -> str`

执行代码生成任务。

**参数:**
- `prompt` (str): 自然语言描述的需求

**返回:**
- `str`: 生成的代码

**示例:**
```python
result = await agent.run("创建一个博客系统")
```

## Model 类

数据库模型管理类。

### 初始化

```python
from mvcgen.models import Model

model = Model(
    name="User",
    fields={
        "id": "int primary key",
        "username": "str unique",
        "email": "str unique"
    }
)
```

### 方法

#### `create(data: dict) -> dict`

创建新记录。

#### `get(id: int) -> dict`

获取单条记录。

#### `update(id: int, data: dict) -> dict`

更新记录。

#### `delete(id: int) -> bool`

删除记录。

#### `list(filters: dict = None) -> list`

获取记录列表。

## 工具函数

### `load_dotenv()`

加载环境变量。

### `format_response(data: dict) -> str`

格式化响应数据。

## 数据模型

### `BaseModel`

Pydantic 基础模型类。

### `UserSchema`

用户数据模型。

### `ResponseSchema`

API 响应模型。 