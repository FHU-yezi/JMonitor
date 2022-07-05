from callbacks import MonitorFailure, MonitorSuccess


def OnSuccessEvent(event) -> None:
    service_name, module_name = event.job_id.split("_")
    success, status_code, error_message = event.retval

    if success:
        MonitorSuccess(service_name, module_name, status_code)
    else:
        MonitorFailure(service_name, module_name, status_code, error_message)


def OnFailureEvent(event) -> None:
    service_name, module_name = event.job_id.split("_")
    status_code = 1001  # 未捕获异常

    MonitorFailure(service_name, module_name, status_code)
