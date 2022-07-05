from code_to_desc import StatusToDesc
from message_sender import (SendServiceReavailableCard,
                            SendServiceUnavailableCard)
from monitor_log_manager import (AddMonitorLog, IsOKLastTime,
                                 IsServiceAndModuleExists)


def MonitorSuccess(service_name: str, module_name: str, status_code: int) -> None:
    status_desc = StatusToDesc(status_code)

    if not IsServiceAndModuleExists(service_name, module_name):  # 第一次记录
        AddMonitorLog(service_name, module_name, True, status_code, status_desc)
        return

    if not IsOKLastTime(service_name, module_name):  # 服务恢复
        SendServiceReavailableCard(service_name, module_name)

    AddMonitorLog(service_name, module_name, True, status_code, status_desc)


def MonitorFailure(service_name: str, module_name: str, status_code: int,
                   error_message: str = "") -> None:
    status_desc = StatusToDesc(status_code)

    if not IsServiceAndModuleExists(service_name, module_name):  # 第一次记录
        AddMonitorLog(service_name, module_name, True, status_code,
                      status_desc, error_message)
        return

    if IsOKLastTime(service_name, module_name):  # 服务故障
        SendServiceUnavailableCard(service_name, module_name, status_code,
                                   status_desc, error_message)

    AddMonitorLog(service_name, module_name, True, status_code,
                  status_desc, error_message)
