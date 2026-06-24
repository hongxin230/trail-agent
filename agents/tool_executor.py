from tools.training_tools import calculate_weekly_volume, suggest_long_run

def run_tool(tool_name: str, params: dict):
    """
    工具分发器（面试重点）
    """

    if tool_name == "calc_weekly":
        return calculate_weekly_volume(**params)

    if tool_name == "long_run":
        return suggest_long_run(**params)

    return {"error": "tool not found"}

    