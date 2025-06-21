<div align="center">
  <h1>MVCGen</h1>
  <strong>基于 LangChain 的智能 MVC 代码生成器</strong>
  <br>
  <p>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"></a>
    <a href="https://jianduo1.github.io/mvcgen/"><img src="https://img.shields.io/badge/docs-latest-blue.svg" alt="Docs"></a>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python Version"></a>
    <img src="https://img.shields.io/badge/LangChain-green.svg" alt="LangChain">
    <a href="https://pypi.org/project/mvcgen/"><img src="https://img.shields.io/badge/pypi-coming%20soon-orange.svg" alt="PyPI"></a>
  </p>
</div>

[中文](README.md) | [English](README_en.md)

**MVCGen** 追求智能、高效、易用，适合快速原型开发、代码生成、自动化开发等场景。

## 1. 特性

- 🚀 **智能代码生成**: 基于自然语言描述自动生成 MVC 架构代码
- 🔧 **多框架支持**: 支持 FastAPI、Django、Flask 等主流 Python Web 框架
- 🗄️ **数据库集成**: 内置 Tortoise ORM 支持，自动生成模型和 CRUD 操作
- 📚 **API 文档**: 自动生成 OpenAPI/Swagger 文档
- ✨ **代码质量**: 集成代码格式化、类型检查
- 🔌 **可扩展性**: 模块化设计，支持自定义工具和模板
- 🎯 **简单易用**: 快速生成 Web 应用代码
- 🔄 **异步支持**: 全异步架构，高性能处理

## 2. 安装

### 2.1 从源码安装

```bash
# 克隆仓库
git clone https://github.com/your-username/mvcgen.git
cd mvcgen

# 安装依赖
pip install -e .

# 开发模式安装
pip install -e ".[dev]"
```

### 2.2 开发环境

```bash
# 安装依赖
pip install -e ".[dev]"

# 运行测试
pytest

# 代码格式化
black .

# 代码检查
flake8

# 运行示例
python examples/basic_example.py
```

## 3. 快速开始

### 3.1 基本使用

```python
from mvcgen import Agent

# 创建 Agent 实例
agent = Agent()

# 生成用户管理模块
result = await agent.run("创建一个用户管理系统，包含用户注册、登录、个人信息管理功能")

print(result)
```

### 3.2 数据库模型生成

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

### 3.3 配置环境变量

创建 `.env` 文件：

```env
# OpenAI API 配置
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# 数据库配置
DATABASE_URL=sqlite://./mvcgen.db

# 应用配置
DEBUG=True
HOST=0.0.0.0
PORT=8000

# 日志配置
LOG_LEVEL=INFO
```

## 4. 高级用法

### 4.1 自定义 Agent 配置

```python
from mvcgen import Agent

# 自定义配置
agent = Agent(
    model_name="gpt-4",
    temperature=0.7,
    max_tokens=2000,
    system_prompt="你是一个专业的 Python 开发者..."
)

result = await agent.run("生成一个博客系统")
```

### 4.2 批量生成

```python
# 批量生成多个模块
modules = [
    "用户管理模块",
    "文章管理模块", 
    "评论系统模块",
    "标签管理模块"
]

for module in modules:
    result = await agent.run(f"创建{module}")
    print(f"生成 {module}: {result}")
```

### 4.3 数据库操作

```python
from mvcgen.models import Model

# 创建记录
user_data = {"username": "john", "email": "john@example.com"}
user = await UserModel.create(user_data)

# 查询记录
users = await UserModel.get_all(filters={"username": "john"})

# 更新记录
await UserModel.update(1, {"email": "new@example.com"})

# 删除记录
await UserModel.delete(1)
```

## 5. 示例项目

### 5.1 博客系统

```python
# 生成完整的博客系统
blog_system = await agent.run("""
创建一个博客系统，包含以下功能：
- 用户注册和登录
- 文章发布和编辑
- 评论系统
- 标签管理
- 搜索功能
- 管理员后台
""")
```

### 5.2 电商系统

```python
# 生成电商系统
ecommerce = await agent.run("""
创建一个电商系统，包含：
- 商品管理
- 购物车
- 订单管理
- 支付集成
- 用户评价
- 库存管理
""")
```

## 6. 项目结构

```
mvcgen/
├── src/mvcgen/
│   ├── __init__.py
│   ├── agent.py          # 核心 Agent 类
│   ├── models.py         # 数据库模型管理
│   ├── schemas.py        # 数据模型定义
│   ├── utils.py          # 工具函数
│   └── dotenv.py         # 环境变量管理
├── examples/             # 示例代码
├── docs/                 # 文档
├── tests/                # 测试文件
├── pyproject.toml        # 项目配置
├── README.md            # 项目说明
└── .env.example         # 环境变量示例
```

## 7. 参考框架

MVCGen 参考和对标了以下主流代码生成和 AI 开发框架：

![LangChain](https://img.shields.io/badge/LangChain-green.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-green.svg) ![Django](https://img.shields.io/badge/Django-green.svg) ![Flask](https://img.shields.io/badge/Flask-green.svg) ![Tortoise ORM](https://img.shields.io/badge/Tortoise%20ORM-green.svg) ![Pydantic](https://img.shields.io/badge/Pydantic-green.svg)

## 8. 项目状态

### 📦 发布状态
- **PyPI**: 🚧 开发中
- **GitHub**: ✅ [开源仓库](https://github.com/your-username/mvcgen)
- **文档**: ✅ [API 文档](docs/api.md) 完整
- **测试**: ✅ 功能测试通过

### 🔄 版本信息
- **当前版本**: 0.1.0
- **Python 支持**: 3.9+
- **许可证**: MIT
- **状态**: Alpha

## 9. 贡献指南

欢迎贡献代码！请查看我们的贡献指南：

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 打开 Pull Request

## 10. 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 11. 相关链接

- [GitHub 仓库](https://github.com/your-username/mvcgen)
- [问题反馈](https://github.com/your-username/mvcgen/issues)
- [讨论区](https://github.com/your-username/mvcgen/discussions)
- [文档](docs/)
- [示例](examples/)

