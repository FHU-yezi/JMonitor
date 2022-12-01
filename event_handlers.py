from callbacks import on_monitor_fail, on_monitor_success


def on_job_success(event) -> None:
    """调度任务成功事件回调

    Args:
        event: 事件对象
    """
    service_name, module_name = event.job_id.split("|")
    success, status_code, error_message = event.retval

    if success:
        on_monitor_success(service_name, module_name, status_code)
    else:
        on_monitor_fail(service_name, module_name, status_code, error_message)


def on_job_fail(event) -> None:
    """调度任务失败事件回调

    Args:
        event: 事件对象
    """
    service_name, module_name = event.job_id.split("|")
    status_code = 1001  # 未捕获异常

    on_monitor_fail(service_name, module_name, status_code)
