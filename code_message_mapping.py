from yaml import SafeLoader
from yaml import load as yaml_load


try:
    with open("code_to_message.yaml", "r", encoding="utf-8") as f:
        mapping = yaml_load(f, Loader=SafeLoader)
except FileNotFoundError:
    # TODO: 记录关键错误日志并终止程序运行
    pass


def GetErrorMessageFromStatusCode(service_name: str, module_name: str,
                                  status_code: int) -> str:
    if service_name in mapping.keys() and \
       module_name in mapping[service_name]:
        special_message = mapping[service_name][module_name].get(status_code)
        if special_message:  # 有针对此服务模块的此状态码定义的错误信息
            return special_message

    return mapping["default"].get(status_code, "未知错误")
