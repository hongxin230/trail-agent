
def calculate_weekly_volume(base_km: int, increase_rate: float = 0.1):
    """
    计算下一周训练量
    """
    next_week = int(base_km * (1 + increase_rate))

    return {
        "base": base_km,
        "next_week": next_week,
        "increase": f"{int(increase_rate*100)}%"
    }


def suggest_long_run(weekly_km: int):
    """
    建议长距离训练
    """
    long_run = int(weekly_km * 0.3)

    return {
        "weekly_km": weekly_km,
        "long_run": long_run
    }

