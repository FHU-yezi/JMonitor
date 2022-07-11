from code_to_desc import StatusToDesc
from message_sender import (SendServiceReavailableCard,
                            SendServiceUnavailableCard)
from monitor_log_manager import (AddMonitorLog, IsOKLastTime,
                                 IsServiceAndModuleExists)
from run_log_manager import AddRunLog


def MonitorSuccess(service_name: str, module_name: str,
                   status_code: int) -> None:
    status_desc = StatusToDesc(status_code)
    AddRunLog("MONITOR", "DEBUG", f"{service_name} {module_name} 运行成功，"
              f"状态码：{status_code}，状态描述：{status_desc}")

    if not IsServiceAndModuleExists(service_name, module_name):  # 第一次记录
        AddMonitorLog(service_name, module_name, True,
                      status_code, status_desc)
        return

    if not IsOKLastTime(service_name, module_name):  # 服务恢复
        AddRunLog("MONITOR", "INFO", f"{service_name} {module_name} "
                  "服务恢复，已发送消息")
        SendServiceReavailableCard(service_name, module_name)

    AddMonitorLog(service_name, module_name, True, status_code, status_desc)


def MonitorFailure(service_name: str, module_name: str, status_code: int,
                   error_message: str = "") -> None:
    status_desc = StatusToDesc(status_code)
    AddRunLog("MONITOR", "DEBUG", f"{service_name} {module_name} 运行失败，"
              f"状态码：{status_code}，状态描述：{status_desc}，"
              f"错误信息：{error_message}")

    if not IsServiceAndModuleExists(service_name, module_name):  # 第一次记录
        AddMonitorLog(service_name, module_name, False, status_code,
                      status_desc, error_message)
        AddRunLog("MONITOR", "INFO", f"{service_name} {module_name} "
                  "服务不可用，已发送消息")
        SendServiceUnavailableCard(service_name, module_name, status_code,
                                   status_desc, error_message)
        return

    if IsOKLastTime(service_name, module_name):  # 服务故障
        AddRunLog("MONITOR", "INFO", f"{service_name} {module_name} "
                  "服务不可用，已发送消息")
        SendServiceUnavailableCard(service_name, module_name, status_code,
                                   status_desc, error_message)

    AddMonitorLog(service_name, module_name, False, status_code,
                  status_desc, error_message)
