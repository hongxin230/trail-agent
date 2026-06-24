
GEAR_KEYWORDS = [
    "鞋",
    "跑鞋",
    "装备",
    "背包",
    "跑杖",
    "手表"
]

def route_intent(text: str) -> str:
    text = text.lower()
    if "训练" in text or "计划" in text:
        return "training"
    for keyword in GEAR_KEYWORDS:
        if keyword in text:
            return "gear"
    return "chat"
