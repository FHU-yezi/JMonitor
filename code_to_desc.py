from yaml import SafeLoader
from yaml import load as yaml_load

from utils.log import run_logger

try:
    with open("code_to_message.yaml", "r", encoding="utf-8") as f:
        mapping = yaml_load(f, Loader=SafeLoader)
except FileNotFoundError:
    run_logger.critical("未找到状态码映射文件 code_to_message.yaml")
    exit(1)


def HTTP_code_to_internal_code(http_status_code: int) -> int:
    """将 HTTP 状态码转换成内部状态码

    Args:
        status_code (int): HTTP 状态码

    Returns:
        int: 内部状态码
    """
    if http_status_code == 200:
        return 0  # 正常
    elif http_status_code == 401:
        return 2001  # 鉴权问题
    elif http_status_code == 403:
        return 2001  # 拒绝服务
    elif 500 <= http_status_code <= 599:
        return 2003  # 服务器故障
    elif http_status_code == 400:
        return 2004  # 请求数据错误
    elif 300 <= http_status_code <= 399:
        return 2005  # 发生重定向
    return 2000  # 未知网络问题


def internal_status_code_to_desc(status_code: int) -> str:
    return mapping[status_code]
