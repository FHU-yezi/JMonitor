from datetime import datetime


def GetNowWithoutMileseconds() -> datetime:
    return datetime.now().replace(microsecond=0)
