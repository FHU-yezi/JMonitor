from functools import wraps
from typing import Callable, List, Tuple

from utils.log import run_logger

_registered_funcs = []


def monitor(service_name: str, module_name: str, cron: str) -> Callable:
    """将函数注册为监控函数

    Args:
        service_name (str, optional): 服务名称
        module_name (str): 服务模块名称
        cron (str, optional): 运行规则 cron 表达式

    Returns:
        Callable: 原函数
    """

    def outer(func: Callable):
        @wraps(func)
        def inner(service_name, module_name, cron):
            _registered_funcs.append((service_name, module_name, cron, func))
            run_logger.debug(
                "成功注册监控函数 " f"{service_name} {module_name}，" f"cron 表达式：{cron}"
            )
            return func

        return inner(service_name, module_name, cron)

    return outer


def get_all_monitors() -> List[Tuple[str, str, str, Callable]]:
    """获取注册的监控函数列表

    Returns:
        List[Tuple[str, str, str, Callable]]: 注册的监控函数列表
    """
    return _registered_funcs
