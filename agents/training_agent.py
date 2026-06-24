from prompts.training_prompts import TRAINING_PROMPT
from app.config import llm
import json
from agents.tool_executor import run_tool


def training_node(state):

    user_input = state["user_input"]

    decision = should_use_tool(user_input)

    metadata = {
        "tool_used": False
    }

    tool_result = None

    if decision.get("use_tool"):

        tool_result = run_tool(
            "calc_weekly",
            {
                "base_km": decision["base_km"],
                "increase_rate": 0.1
            }
        )

        metadata["tool_used"] = True
        metadata["tool_result"] = tool_result

    prompt = TRAINING_PROMPT.format(
        input=user_input,
        tool_result=json.dumps(tool_result, ensure_ascii=False)
        if tool_result else "无"
    )

    resp = llm.invoke(prompt)

    try:
        content = resp.content.strip()
        if content.startswith("```"):
            content = content.split("\n", 1)[1].rsplit("\n", 1)[0]
            if content.startswith("```"):
                content = content[3:].strip()
        plan = json.loads(content)

    except Exception as e:
        plan = {
            "error": "json_parse_failed",
            "raw_output": resp.content
        }

    return {
        "response": {
            "type": "training_plan",
            "data": plan,
            "metadata": metadata
        }
    }

def should_use_tool(user_input: str):
    prompt = f"""
判断是否需要计算训练量。

用户输入：
{user_input}

仅返回JSON：

{{
    "use_tool": true,
    "base_km": 40
}}
"""

    resp = llm.invoke(prompt)

    try:
        return json.loads(resp.content)
    except:
        return {
            "use_tool": False
        }