from fastapi import FastAPI, HTTPException
from tortoise.contrib.fastapi import register_tortoise
from mvcgen.src.mvcgen.models import Model
from mvcgen.src.mvcgen.utils import Int, Char, Text, Json, Datetime, FK, M2M
from mvcgen.src.mvcgen.agent import Agent

# 创建 FastAPI 应用
app = FastAPI(title="MVCGen API")

# 定义模型
class Project(Model):
    """项目模型，用于管理项目信息"""
    id = Int(pk=True)
    name = Char(max_length=100)
    description = Text()
    created_at = Datetime(auto_now_add=True)
    updated_at = Datetime(auto_now=True)

class Context(Model):
    """上下文模型，用于存储对话上下文"""
    id = Int(pk=True)
    project = FK(Project)
    content = Json()
    created_at = Datetime(auto_now_add=True)

# 创建 MVCGen 代理实例
agent = Agent([Project, Context])

# 注册 Tortoise ORM
register_tortoise(
    app,
    db_url='sqlite://db.sqlite3',
    modules={'models': ['mvcgen.examples.fastapi_example']},
    generate_schemas=True,
    add_exception_handlers=True,
)

@app.post("/query")
async def query(query: str):
    """处理自然语言查询"""
    try:
        result = await agent.run(query)
        return {"result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/models")
async def list_models():
    """列出所有可用模型"""
    return {
        "models": [
            {
                "name": model.__name__,
                "description": model.__doc__,
                "fields": [
                    {
                        "name": name,
                        "type": str(field.__class__.__name__),
                        "description": field.description if hasattr(field, "description") else None
                    }
                    for name, field in model._meta.fields.items()
                ]
            }
            for model in agent.models
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 