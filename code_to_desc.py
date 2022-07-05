from yaml import SafeLoader
from yaml import load as yaml_load

from run_log_manager import AddRunLog

try:
    with open("code_to_message.yaml", "r", encoding="utf-8") as f:
        mapping = yaml_load(f, Loader=SafeLoader)
except FileNotFoundError:
    AddRunLog("SYSTEM", "CRITICAL", "未找到状态信息映射文件 code_to_message.yaml")
    pass


def HTTPStatusCodeConvert(status_code: int) -> int:
    if status_code == 200:
        return 0  # 正常
    elif status_code == 401:
        return 2001  # 鉴权问题
    elif status_code == 403:
        return 2001  # 拒绝服务
    elif 500 <= status_code <= 599:
        return 2003  # 服务器故障
    elif status_code == 400:
        return 2004  # 请求数据错误
    elif 300 <= status_code <= 399:
        return 2005  # 发生重定向
    return 2000  # 未知网络问题


def StatusToDesc(status_code: int) -> str:
    return mapping[status_code]