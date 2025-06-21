<div align="center">
  <h1>MVCGen</h1>
  <strong>An intelligent MVC code generator based on LangChain</strong>
  <br>
  <p>
    <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License"></a>
    <a href="https://jianduo1.github.io/mvcgen/"><img src="https://img.shields.io/badge/docs-latest-blue.svg" alt="Docs"></a>
    <a href="https://www.python.org/downloads/"><img src="https://img.shields.io/badge/python-3.9+-blue.svg" alt="Python Version"></a>
    <img src="https://img.shields.io/badge/LangChain-green.svg" alt="LangChain">
    <a href="https://pypi.org/project/mvcgen/"><img src="https://img.shields.io/badge/pypi-coming%20soon-orange.svg" alt="PyPI"></a>
  </p>
</div>

[中文](README.md) | English

**MVCGen** pursues intelligence, efficiency, and ease of use, suitable for rapid prototyping, code generation, and automated development scenarios.

## 1. Features

- 🚀 **Intelligent Code Generation**: Automatically generate MVC architecture code based on natural language descriptions
- 🔧 **Multi-Framework Support**: Support mainstream Python Web frameworks like FastAPI, Django, Flask
- 🗄️ **Database Integration**: Built-in Tortoise ORM support, auto-generate models and CRUD operations
- 📚 **API Documentation**: Automatically generate OpenAPI/Swagger documentation
- ✨ **Code Quality**: Integrated code formatting, type checking
- 🔌 **Extensibility**: Modular design, support custom tools and templates
- 🎯 **Easy to Use**: Quickly generate Web application code
- 🔄 **Async Support**: Full asynchronous architecture, high-performance processing

## 2. Installation

### 2.1 Install from Source

```bash
# Clone repository
git clone https://github.com/your-username/mvcgen.git
cd mvcgen

# Install dependencies
pip install -e .

# Install in development mode
pip install -e ".[dev]"
```

### 2.2 Development Environment

```bash
# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .

# Code linting
flake8

# Run examples
python examples/basic_example.py
```

## 3. Quick Start

### 3.1 Basic Usage

```python
from mvcgen import Agent

# Create Agent instance
agent = Agent()

# Generate user management module
result = await agent.run("Create a user management system with user registration, login, and profile management")

print(result)
```

### 3.2 Database Model Generation

```python
from mvcgen.models import Model

# Create user model
user_model = Model("User", {
    "id": "int primary key",
    "username": "str unique",
    "email": "str unique",
    "password": "str",
    "created_at": "datetime"
})

# Generate CRUD operations
crud_code = await user_model.generate_crud()
```

### 3.3 Environment Configuration

Create `.env` file:

```env
# OpenAI API Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_BASE_URL=https://api.openai.com/v1

# Database Configuration
DATABASE_URL=sqlite://./mvcgen.db

# Application Configuration
DEBUG=True
HOST=0.0.0.0
PORT=8000

# Logging Configuration
LOG_LEVEL=INFO
```

## 4. Advanced Usage

### 4.1 Custom Agent Configuration

```python
from mvcgen import Agent

# Custom configuration
agent = Agent(
    model_name="gpt-4",
    temperature=0.7,
    max_tokens=2000,
    system_prompt="You are a professional Python developer..."
)

result = await agent.run("Generate a blog system")
```

### 4.2 Batch Generation

```python
# Batch generate multiple modules
modules = [
    "User Management Module",
    "Article Management Module", 
    "Comment System Module",
    "Tag Management Module"
]

for module in modules:
    result = await agent.run(f"Create {module}")
    print(f"Generated {module}: {result}")
```

### 4.3 Database Operations

```python
from mvcgen.models import Model

# Create record
user_data = {"username": "john", "email": "john@example.com"}
user = await UserModel.create(user_data)

# Query records
users = await UserModel.get_all(filters={"username": "john"})

# Update record
await UserModel.update(1, {"email": "new@example.com"})

# Delete record
await UserModel.delete(1)
```

## 5. Example Projects

### 5.1 Blog System

```python
# Generate complete blog system
blog_system = await agent.run("""
Create a blog system with the following features:
- User registration and login
- Article publishing and editing
- Comment system
- Tag management
- Search functionality
- Admin backend
""")
```

### 5.2 E-commerce System

```python
# Generate e-commerce system
ecommerce = await agent.run("""
Create an e-commerce system with:
- Product management
- Shopping cart
- Order management
- Payment integration
- User reviews
- Inventory management
""")
```

## 6. Project Structure

```
mvcgen/
├── src/mvcgen/
│   ├── __init__.py
│   ├── agent.py          # Core Agent class
│   ├── models.py         # Database model management
│   ├── schemas.py        # Data model definitions
│   ├── utils.py          # Utility functions
│   └── dotenv.py         # Environment variable management
├── examples/             # Example code
├── docs/                 # Documentation
├── tests/                # Test files
├── pyproject.toml        # Project configuration
├── README.md            # Project description
└── .env.example         # Environment variable example
```

## 7. Reference Frameworks

MVCGen references and benchmarks against the following mainstream code generation and AI development frameworks:

![LangChain](https://img.shields.io/badge/LangChain-green.svg) ![FastAPI](https://img.shields.io/badge/FastAPI-green.svg) ![Django](https://img.shields.io/badge/Django-green.svg) ![Flask](https://img.shields.io/badge/Flask-green.svg) ![Tortoise ORM](https://img.shields.io/badge/Tortoise%20ORM-green.svg) ![Pydantic](https://img.shields.io/badge/Pydantic-green.svg)

## 8. Project Status

### 📦 Release Status
- **PyPI**: 🚧 In Development
- **GitHub**: ✅ [Open Source Repository](https://github.com/your-username/mvcgen)
- **Documentation**: ✅ [API Documentation](docs/api.md) Complete
- **Testing**: ✅ Functional tests passed

### 🔄 Version Information
- **Current Version**: 0.1.0
- **Python Support**: 3.9+
- **License**: MIT
- **Status**: Alpha

## 9. Contributing

Welcome to contribute code! Please check our contributing guidelines:

1. Fork the project
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 10. License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 11. Related Links

- [GitHub Repository](https://github.com/your-username/mvcgen)
- [Issue Tracker](https://github.com/your-username/mvcgen/issues)
- [Discussions](https://github.com/your-username/mvcgen/discussions)
- [Documentation](docs/)
- [Examples](examples/) 