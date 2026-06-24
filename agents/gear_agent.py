import json

from app.config import llm

from rag.vector_store import search_gear

from prompts.gear_prompt import GEAR_PROMPT


def gear_node(state):

    user_input = state["user_input"]

    # Step1: 检索相关装备
    context = search_gear(user_input)

    # Step2: LLM 生成推荐
    prompt = GEAR_PROMPT.format(
        question=user_input,
        context=context,
    )

    resp = llm.invoke(prompt)
    content = resp.content

    # Step3: 尝试解析 JSON，失败则原样返回
    try:
        json.loads(content)
    except Exception:
        pass

    return {"response": content}