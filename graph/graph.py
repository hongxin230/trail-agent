from dotenv import load_dotenv
from langgraph.graph import StateGraph

from app.config import llm
from graph.state import AgentState
from agents.router import route_intent
from agents.training_agent import training_node
from rag.vector_store import search_gear
from agents.gear_agent import gear_node

load_dotenv()

def router_node(state: AgentState) -> AgentState:
    user_input = state["user_input"]
    intent = route_intent(user_input)
    return {"intent": intent}

def chat_node(state: AgentState) -> AgentState:
    """
    state = {
        "user_input": str,
        "intent": str,
        "response": str
    }
    """

    user_input = state["user_input"]

    # 3. 调用大模型
    resp = llm.invoke([
        ("system", "你是一个专业越野跑AI教练，回答要简洁、实用"),
        ("user", user_input)
    ])

    # 4. LangGraph要求：返回“更新后的state字段”
    return {
        "response": resp.content
    }

# 路由逻辑
def route_selector(state: AgentState) -> str:
    return state["intent"]

def build_graph():
    workflow = StateGraph(AgentState)

    workflow.add_node("router", router_node)
    workflow.add_node("training", training_node)
    workflow.add_node("gear", gear_node)
    workflow.add_node("chat", chat_node)

    workflow.set_entry_point("router")

    workflow.add_conditional_edges(
        "router",
        route_selector,
        {
            "chat": "chat",
            "training": "training",
            "gear": "gear"
        }
    )
    
    workflow.add_edge("chat", END)
    workflow.add_edge("training", END)
    workflow.add_edge("gear", END)

    return workflow.compile()
