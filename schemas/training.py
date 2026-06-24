from typing import TypedDict, List

class TrainingPlan(TypedDict):
    goal: str
    weeks: List[dict]