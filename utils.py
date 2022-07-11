from datetime import datetime
from typing import Dict


def GetNowWithoutMileseconds() -> datetime:
    return datetime.now().replace(microsecond=0)


def CronToKwargs(cron: str) -> Dict[str, str]:
    """将 Cron 表达式转换成 Apscheduler 可识别的参数组

    Args:
        cron (str): cron 表达式

    Returns:
        Dict[str, str]: 参数组
    """
    second, minute, hour, day, month, day_of_week = cron.split()
    result = {"second": second,
              "minute": minute,
              "hour": hour,
              "day": day,
              "month": month,
              "day_of_week": day_of_week}
    return result
