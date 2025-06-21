# 快速开始

## 安装

```bash
pip install mvcgen
```

## 基本使用

### 1. 创建 Agent 实例

```python
from mvcgen import Agent

# 创建 Agent 实例
agent = Agent()
```

### 2. 生成 MVC 代码

```python
# 生成用户管理模块
result = await agent.run("创建一个用户管理系统，包含用户注册、登录、个人信息管理功能")

print(result)
```

### 3. 数据库操作

```python
from mvcgen.models import Model

# 创建用户模型
user_model = Model("User", {
    "id": "int primary key",
    "username": "str unique",
    "email": "str unique",
    "password": "str",
    "created_at": "datetime"
})

# 生成 CRUD 操作
crud_code = await user_model.generate_crud()
```

## 配置

创建 `.env` 文件：

```env
# OpenAI API 配置
OPENAI_API_KEY=your_openai_api_key_here

# 数据库配置
DATABASE_URL=sqlite://./mvcgen.db

# 应用配置
DEBUG=True
PORT=8000
```

## 示例项目

查看 `examples/` 目录获取更多示例代码。 