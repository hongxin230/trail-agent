from langchain_openai import ChatOpenAI
from config import DEEPSEEK_API_KEY

llm = config.client

def chat_node(state):
    user_input = state["user_input"]

    resp = llm.invoke([
        ("system", "你是一个专业越野跑AI教练"),
        ("user", user_input)
    ])

    return {
        "response": resp.content
    }