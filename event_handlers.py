from callbacks import MonitorFailure, MonitorSuccess


def OnSuccessEvent(event) -> None:
    """调度任务成功事件回调

    Args:
        event: 事件对象
    """
    service_name, module_name = event.job_id.split("|")
    success, status_code, error_message = event.retval

    if success:
        MonitorSuccess(service_name, module_name, status_code)
    else:
        MonitorFailure(service_name, module_name, status_code, error_message)


def OnFailureEvent(event) -> None:
    """调度任务失败事件回调

    Args:
        event: 事件对象
    """
    service_name, module_name = event.job_id.split("|")
    status_code = 1001  # 未捕获异常

    MonitorFailure(service_name, module_name, status_code)
