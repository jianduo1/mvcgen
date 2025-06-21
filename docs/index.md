# MVCGen

<div align="center">

![MVCGen Logo](https://img.shields.io/badge/MVCGen-AI%20Code%20Generator-blue?style=for-the-badge&logo=python)

**基于 LangChain 的智能 MVC 代码生成器**

[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![PyPI](https://img.shields.io/badge/pypi-mvcgen-blue.svg)](https://pypi.org/project/mvcgen/)

</div>

## 🚀 特性

- **智能代码生成**: 基于自然语言描述自动生成 MVC 架构代码
- **多框架支持**: 支持 FastAPI、Django、Flask 等主流 Python Web 框架
- **数据库集成**: 内置 Tortoise ORM 支持，自动生成模型和迁移文件
- **API 文档**: 自动生成 OpenAPI/Swagger 文档
- **代码质量**: 集成代码格式化、类型检查和测试框架
- **可扩展性**: 模块化设计，支持自定义工具和模板

## 📦 快速安装

```bash
pip install mvcgen
```

## 🎯 快速开始

```python
from mvcgen import Agent

# 创建 Agent 实例
agent = Agent()

# 生成用户管理模块
result = await agent.run("创建一个用户管理系统，包含用户注册、登录、个人信息管理功能")

print(result)
```

## 📚 文档

- [快速开始](getting-started.md)
- [API 参考](api.md)

## 🤝 贡献

欢迎贡献代码！请查看我们的 [GitHub 仓库](https://github.com/your-username/mvcgen)。

## 📄 许可证

本项目采用 MIT 许可证。

## 🔗 相关链接

- [GitHub 仓库](https://github.com/your-username/mvcgen)
- [问题反馈](https://github.com/your-username/mvcgen/issues) 