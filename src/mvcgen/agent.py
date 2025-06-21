import json
import traceback
from typing import Dict, Any, List, Type, Annotated, TypedDict
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain_openai.chat_models import ChatOpenAI
from langgraph.graph.state import CompiledStateGraph
from langgraph.graph import StateGraph, END, add_messages
from pydantic import BaseModel as PydanticModel, Field as PydanticField
from .models import Model

class Agent:
    def __init__(self, models: List[Type[Model]], llm=None):
        self.models: List[type[Model]] = models
        self.llm = llm or self._get_default_llm()
        self.graph: CompiledStateGraph = self._build_graph()

    def _get_model_prompt(self):
        prompt = ""
        for model in self.models:
            prompt += f"{model.__doc__.replace('\n', ' ')} {model.__name__}{model.create_schema.__signature__}\n"
        return prompt

    def _get_default_llm(self):
        return ChatOpenAI(model="gpt-4o-mini")

    def _build_graph(self):
        class AgentState(TypedDict):
            messages: Annotated[list, add_messages]
            current_model: str
            operation: str
            params: dict
            result: str
            error: str
            confirmed: bool

        builder = StateGraph(AgentState)
        builder.add_node("parse_intent", self._parse_intent)
        builder.add_node("confirm_operation", self._confirm_operation)
        builder.add_node("execute_operation", self._execute_operation)
        builder.add_node("format_response", self._format_response)
        builder.add_edge("parse_intent", "confirm_operation")
        builder.add_conditional_edges("confirm_operation", lambda x: "execute_operation" if x["confirmed"] else END, ["execute_operation", END])
        builder.add_edge("execute_operation", "format_response")
        builder.add_edge("format_response", END)
        builder.set_entry_point("parse_intent")
        return builder.compile()

    async def _parse_intent(self, state: dict):
        class Intent(PydanticModel):
            model: str = PydanticField(description="要操作的模型名称")
            operation: str = PydanticField(description="要执行的操作类型(create/read/update/delete)")
            params: Dict[str, Any] = PydanticField(description="操作的具体参数")

        last_message = state["messages"][-1]
        system_prompt = f"""你是一个数据库操作助手。你需要从用户输入中识别:
1. 要操作的模型名称
2. 要执行的操作类型(create/read/update/delete)
3. 操作的具体参数

可用的模型有:
{self._get_model_prompt()}

请以JSON格式返回结果，格式如下:
{{
    "model": "模型名称",
    "operation": "操作类型",
    "params": {{操作参数}}
}}

注意：
1. 当参数值为None时，直接使用null而不是字符串"None"
2. 对于关联字段（如parent、env），如果值为None，使用null
"""

        messages = [SystemMessage(content=system_prompt), HumanMessage(content=last_message.content)]
        print("\n🔍 解析意图\n")
        for msg in messages:
            msg.pretty_print()

        try:
            response: Intent = await self.llm.with_structured_output(Intent).ainvoke(messages)
            print("\n🔍 解析结果\n", response.model_dump())
            state["current_model"] = response.model
            state["operation"] = response.operation
            state["params"] = response.params
            state["confirmed"] = False
            state["error"] = None
        except Exception as e:
            state["error"] = f"无法解析操作意图: {str(e)}"
            state["current_model"] = None
            state["operation"] = None
            state["params"] = {}
            state["confirmed"] = False
        return state

    async def _confirm_operation(self, state: dict):
        if state.get("error"):
            return state
        confirm_message = f"""
🔍 请确认以下操作:

模型: {state.get('current_model', '未知')}
操作: {state.get('operation', '未知')}
参数: {json.dumps(state.get('params', {}), ensure_ascii=False, indent=2)}

是否执行此操作? (y/n)"""
        try:
            user_input = input(confirm_message).strip().lower()
            if user_input == 'y':
                state["confirmed"] = True
            else:
                state["confirmed"] = False
                state["error"] = "用户取消了操作或输入了无效的回答"
                state["result"] = None
        except Exception as e:
            state["error"] = f"用户交互失败: {str(e)}"
            state["confirmed"] = False
            state["result"] = None
        return state

    async def _execute_operation(self, state: dict):
        try:
            model = next((m for m in self.models if m.__name__ == state["current_model"]), None)
            if not model:
                state["error"] = f"找不到模型: {state['current_model']}"
                return state

            operation = state["operation"]
            params = state["params"]

            print("\n🚀 执行操作\n")
            print(f"模型: {model.__name__}")
            print(f"操作: {operation}")
            print(f"参数: {params}")

            if operation == "create":
                try:
                    result = await model.create(params)
                except Exception as e:
                    state["error"] = f"创建操作失败: {str(e)}\n参数: {params}\n错误堆栈: {traceback.format_exc()}"
                    return state
            elif operation == "read":
                try:
                    if "id" in params:
                        result = await model.get(params["id"])
                    else:
                        result = await model.get_all(**params)
                except Exception as e:
                    state["error"] = f"读取操作失败: {str(e)}\n参数: {params}"
                    return state
            elif operation == "update":
                if "id" not in params:
                    state["error"] = "更新操作需要提供id"
                    return state
                try:
                    id = params.pop("id")
                    result = await model.update(id, params)
                except Exception as e:
                    state["error"] = f"更新操作失败: {str(e)}\nID: {id}\n参数: {params}"
                    return state
            elif operation == "delete":
                if "id" not in params:
                    state["error"] = "删除操作需要提供id"
                    return state
                try:
                    result = await model.delete(params["id"])
                except Exception as e:
                    state["error"] = f"删除操作失败: {str(e)}\nID: {params['id']}"
                    return state
            else:
                state["error"] = f"不支持的操作类型: {operation}"
                return state

            state["result"] = result
        except Exception as e:
            error_traceback = traceback.format_exc()
            state["error"] = f"操作执行失败:\n错误信息: {str(e)}\n错误堆栈:\n{error_traceback}"
        return state

    async def _format_response(self, state: dict):
        if state.get("error"):
            response = f"操作失败: {state['error']}"
        elif state.get("result") is None:
            response = "操作成功，但未返回数据"
        else:
            response = f"操作成功: {state['result']}"
        print("\n🎉 操作结果\n", response)
        return state

    async def run(self, query: str):
        state = {
            "messages": [HumanMessage(content=query)],
            "current_model": None,
            "operation": None,
            "params": {},
            "result": None,
            "error": None,
            "confirmed": False,
        }
        result = await self.graph.ainvoke(state)
        return result["messages"][-1].content 