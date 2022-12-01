from datetime import datetime

from utils.db import monitor_log_db
from utils.log import run_logger
from utils.time_helper import get_now_without_mileseconds


def add_monitor_log(
    service_name: str,
    module_name: str,
    OK: bool,
    status_code: int,
    status_desc: str,
    error_message: str = "",
) -> None:
    """添加监控任务日志记录

    Args:
        service_name (str): 服务名称
        module_name (str): 模块名称
        OK (bool): 是否正常
        status_code (int): 状态码
        status_desc (str): 状态描述
        error_message (str, optional): 错误信息. Defaults to "".
    """
    monitor_log_db.insert_one(
        {
            "time": get_now_without_mileseconds(),
            "service_name": service_name,
            "module_name": module_name,
            "OK": OK,
            "status_code": status_code,
            "status_desc": status_desc,
            "error_message": error_message,
        }
    )


def is_service_and_module_exists(service_name: str, module_name: str) -> bool:
    """判断服务和模块是否存在

    Args:
        service_name (str): 服务名称
        module_name (str): 模块名称

    Returns:
        bool: 是否存在
    """
    if (
        monitor_log_db.count_documents(
            {
                "service_name": service_name,
                "module_name": module_name,
            }
        )
        > 0
    ):
        return True
    return False


def is_OK_last_time(service_name: str, module_name: str) -> bool:
    """判断服务和模块上次是否为正常状态

    Args:
        service_name (str): 服务名称
        module_name (str): 模块名称

    Raises:
        ValueError: 服务或模块不存在

    Returns:
        bool: 是否正常
    """
    if not is_service_and_module_exists(service_name, module_name):
        run_logger.error(f"{service_name} {module_name} 不存在")
        raise ValueError("服务或模块不存在")

    return (
        monitor_log_db.find(
            {
                "service_name": service_name,
                "module_name": module_name,
            },
            {
                "_id": 0,
                "OK": 1,
            },
        )
        .sort("time", -1)
        .limit(1)[0]["OK"]
    )


def get_last_OK_time(service_name: str, module_name: str) -> datetime:
    """获取服务和模块上次执行成功的时间

    Args:
        service_name (str): 服务名称
        module_name (str): 模块名称

    Raises:
        ValueError: 服务或模块不存在
        ValueError: 监控任务没有成功过

    Returns:
        datetime: 上一次成功时间
    """
    if not is_service_and_module_exists(service_name, module_name):
        run_logger.error(f"{service_name} {module_name} 不存在")
        raise ValueError("服务或模块不存在")

    cursor = (
        monitor_log_db.find(
            {
                "service_name": service_name,
                "module_name": module_name,
                "OK": True,
            },
            {
                "_id": 0,
                "time": 1,
            },
        )
        .sort("time", -1)
        .limit(1)
    )

    try:
        return cursor[0]["time"]
    except IndexError:
        raise ValueError("该监控任务没有成功过")


def get_last_fail_time(service_name: str, module_name: str) -> datetime:
    """获取服务和模块上次执行失败的时间

    Args:
        service_name (str): 服务名称
        module_name (str): 模块名称

    Raises:
        ValueError: 服务或模块不存在
        ValueError: 监控任务没有失败过

    Returns:
        datetime: 上一次失败时间
    """
    if not is_service_and_module_exists(service_name, module_name):
        run_logger.error(
            f"{service_name} {module_name} 不存在"
        )
        raise ValueError("服务或模块不存在")

    cursor = (
        monitor_log_db.find(
            {
                "service_name": service_name,
                "module_name": module_name,
                "OK": False,
            },
            {
                "_id": 0,
                "time": 1,
            },
        )
        .sort("time", -1)
        .limit(1)
    )

    try:
        return cursor[0]["time"]
    except IndexError:
        raise ValueError("该监控任务没有失败过")


def get_last_target_status_code_time(
    service_name: str, module_name: str, status_code: int
) -> datetime:
    """获取服务和模块上次返回此状态码的时间

    Args:
        service_name (str): 服务名称
        module_name (str): 模块名称
        status_code (int): 状态码

    Raises:
        ValueError: 服务或模块不存在
        ValueError: 该监控任务没有出现过此状态码

    Returns:
        datetime: 上次出现该状态码的时间
    """
    if not is_service_and_module_exists(service_name, module_name):
        run_logger.error(
            f"{service_name} {module_name} 不存在"
        )
        raise ValueError("服务或模块不存在")

    cursor = (
        monitor_log_db.find(
            {
                "service_name": service_name,
                "module_name": module_name,
                "status_code": status_code,
            },
            {
                "_id": 0,
                "time": 1,
            },
        )
        .sort("time", -1)
        .limit(1)
    )

    try:
        return cursor[0]["time"]
    except IndexError:
        raise ValueError("该监控任务没有出现过此状态码")
