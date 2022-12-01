from code_to_desc import StatusToDesc
from utils.message import send_service_reavailable_card, send_service_unavailable_card
from monitor_log_manager import (AddMonitorLog, IsOKLastTime,
                                 IsServiceAndModuleExists)
from utils.log import run_logger


def MonitorSuccess(service_name: str, module_name: str,
                   status_code: int) -> None:
    """监控任务成功回调

    Args:
        service_name (str): 服务名称
        module_name (str): 模块名称
        status_code (int): 状态码
    """
    status_desc = StatusToDesc(status_code)
    run_logger.debug(f"{service_name} {module_name} 运行成功，"
              f"状态码：{status_code}，状态描述：{status_desc}")

    if not IsServiceAndModuleExists(service_name, module_name):  # 第一次记录
        AddMonitorLog(service_name, module_name, True,
                      status_code, status_desc)
        return

    if not IsOKLastTime(service_name, module_name):  # 服务恢复
        run_logger.info(f"{service_name} {module_name} "
                  "服务恢复，已发送消息")
        send_service_reavailable_card(service_name, module_name)

    AddMonitorLog(service_name, module_name, True, status_code, status_desc)


def MonitorFailure(service_name: str, module_name: str, status_code: int,
                   error_message: str = "") -> None:
    """监控任务失败回调

    Args:
        service_name (str): 服务名称
        module_name (str): 模块名称
        status_code (int): 状态码
        error_message (str, optional): 错误信息. Defaults to "".
    """
    status_desc = StatusToDesc(status_code)
    run_logger.debug(f"{service_name} {module_name} 运行失败，"
              f"状态码：{status_code}，状态描述：{status_desc}，"
              f"错误信息：{error_message}")

    if not IsServiceAndModuleExists(service_name, module_name):  # 第一次记录
        AddMonitorLog(service_name, module_name, False, status_code,
                      status_desc, error_message)
        run_logger.info(f"{service_name} {module_name} "
                  "服务不可用，已发送消息")
        send_service_unavailable_card(service_name, module_name, status_code,
                                   status_desc, error_message)
        return

    if IsOKLastTime(service_name, module_name):  # 服务故障
        run_logger.info("{service_name} {module_name} "
                  "服务不可用，已发送消息")
        send_service_unavailable_card(service_name, module_name, status_code,
                                   status_desc, error_message)

    AddMonitorLog(service_name, module_name, False, status_code,
                  status_desc, error_message)
