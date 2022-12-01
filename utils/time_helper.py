from datetime import datetime
from typing import Dict


def get_now_without_mileseconds() -> datetime:
    return datetime.now().replace(microsecond=0)


def human_readable_time_cost(cost_time: int) -> str:
    """将耗时转换成人类可读格式

    Args:
        cost_time (int): 耗时，单位为秒

    Returns:
        str: 人类可读格式的耗时字符串
    """
    MAPPING = {
        "分": 60,
        "秒": 1,
    }
    data = {key: 0 for key in MAPPING.keys()}

    for key, value in MAPPING.items():
        while value <= cost_time:
            data[key] += 1
            cost_time -= value

    if sum(data.values()) == 0:
        return "0秒"

    if data["分"] == 0 and data["秒"] != 0:
        del data["分"]

    return "".join(f"{value}{key}" for key, value in data.items())


def cron_to_kwargs(cron: str) -> Dict[str, str]:
    """将 Cron 表达式转换成 Apscheduler 可识别的参数组

    Args:
        cron (str): cron 表达式

    Returns:
        Dict[str, str]: 参数组
    """
    second, minute, hour, day, month, day_of_week = cron.split()
    result = {
        "second": second,
        "minute": minute,
        "hour": hour,
        "day": day,
        "month": month,
        "day_of_week": day_of_week,
    }
    return result
