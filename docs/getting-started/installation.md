# 安装指南

## 系统要求

- Python 3.9 或更高版本
- pip 包管理器
- Git（可选，用于从源码安装）

## 安装方法

### 方法一：从 PyPI 安装（推荐）

```bash
pip install mvcgen
```

### 方法二：从源码安装

```bash
# 克隆仓库
git clone https://github.com/your-username/mvcgen.git
cd mvcgen

# 安装依赖
pip install -e .
```

### 方法三：使用 conda 安装

```bash
conda install -c conda-forge mvcgen
```

## 验证安装

安装完成后，可以通过以下方式验证：

```python
import mvcgen
print(mvcgen.__version__)
```

或者在命令行中：

```bash
python -c "import mvcgen; print(mvcgen.__version__)"
```

## 依赖项

MVCGen 的主要依赖项包括：

- **langchain-core**: LangChain 核心功能
- **fastapi**: Web 框架
- **tortoise-orm**: 异步 ORM
- **pydantic**: 数据验证
- **python-dotenv**: 环境变量管理

## 开发环境设置

如果你想要贡献代码或进行开发，建议设置开发环境：

```bash
# 克隆仓库
git clone https://github.com/your-username/mvcgen.git
cd mvcgen

# 创建虚拟环境
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
venv\Scripts\activate  # Windows

# 安装开发依赖
pip install -e ".[dev]"

# 安装预提交钩子
pre-commit install
```

## 配置环境变量

创建 `.env` 文件并配置必要的环境变量：

```bash
cp .env.example .env
```

编辑 `.env` 文件，设置你的 API 密钥和其他配置：

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
```

## 故障排除

### 常见问题

1. **ImportError: No module named 'mvcgen'**
   - 确保已正确安装包
   - 检查 Python 环境是否正确

2. **API 密钥错误**
   - 确保在 `.env` 文件中设置了正确的 `OPENAI_API_KEY`
   - 验证 API 密钥是否有效

3. **数据库连接错误**
   - 检查 `DATABASE_URL` 配置
   - 确保数据库服务正在运行

### 获取帮助

如果遇到其他问题，请：

1. 查看 [GitHub Issues](https://github.com/your-username/mvcgen/issues)
2. 在 [GitHub Discussions](https://github.com/your-username/mvcgen/discussions) 中提问
3. 查看 [API 文档](api/agent.md) 获取详细信息 