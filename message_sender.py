from typing import Dict

from httpx import post as httpx_post

from run_log_manager import AddRunLog
from utils import GetNowWithoutMileseconds
from utils.config import config


def GetFeishuToken() -> str:
    """获取飞书 Token

    Raises:
        ValueError: 获取 Token 失败

    Returns:
        str: 飞书 Token
    """
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "app_id": config.message_sender.app_id,
        "app_secret": config.message_sender.app_secret
    }
    response = httpx_post("https://open.feishu.cn/open-apis/auth/v3/"
                          "tenant_access_token/internal",
                          headers=headers, json=data)
    if response.json()["code"] == 0:
        return "Bearer " + response.json()["tenant_access_token"]
    else:
        AddRunLog("SENDER", "ERROR", "获取 Token 时发生错误，错误码："
                  f"{response.json()['code']}，错误信息：{response.json()['msg']}")
        raise ValueError("获取 Token 时发生错误，"
                         f"错误码：{response.json()['code']}，"
                         f"错误信息：{response.json()['msg']}")


def SendFeishuCard(card: Dict) -> None:
    """发送飞书卡片

    Args:
        card (Dict): 飞书卡片

    Raises:
        ValueError: 发送飞书卡片失败
    """
    token = GetFeishuToken()
    headers = {"Content-Type": "application/json; charset=utf-8",
               "Authorization": token}

    data = {
        "email": config.message_sender.email,
        "msg_type": "interactive",
        "card": card
    }
    response = httpx_post("https://open.feishu.cn/open-apis/message/v4/send/",
                          headers=headers, json=data)
    if response.json()["code"] != 0:
        AddRunLog("SENDER", "ERROR", "发送消息卡片时发生错误，"
                  f"错误码：{response.json()['code']}，"
                  f"错误信息：{response.json()['msg']}")
        raise ValueError("发送消息卡片时发生错误，"
                         f"错误码：{response.json()['code']}，"
                         f"错误信息：{response.json()['msg']}")


def SendServiceUnavailableCard(service_name: str, module_name: str,
                               status_code: int, status_desc: str,
                               error_message: str) -> None:
    """发送服务不可用卡片

    Args:
        service_name (str): 服务名称
        module_name (str): 模块名称
        status_code (int): 状态码
        status_desc (str): 状态描述
        error_message (str): 错误信息
    """
    time_now = GetNowWithoutMileseconds()

    card = {
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "服务不可用告警"
            },
            "template": "red"
        },
        "elements": [
            {
                "tag": "markdown",
                "content": f"**时间：**{time_now}"
            },
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": f"**服务名**\n{service_name}"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": f"**功能模块**\n{module_name}"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": ""
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": f"**状态码**\n{status_code}"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": f"**状态描述**\n{status_desc}"
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": ""
                        }
                    },
                    {
                        "is_short": False,
                        "text": {
                            "tag": "lark_md",
                            "content": f"**错误信息**\n{error_message}"
                        }
                    }
                ]
            }
        ]
    }

    SendFeishuCard(card)


def SendServiceReavailableCard(service_name: str, module_name: str) -> None:
    """发送服务恢复卡片

    Args:
        service_name (str): 服务名称
        module_name (str): 模块名称
    """
    time_now = GetNowWithoutMileseconds()

    card = {
        "header": {
            "title": {
                "tag": "plain_text",
                "content": "服务恢复提示"
            },
            "template": "green"
        },
        "elements": [
            {
                "tag": "markdown",
                "content": f"**时间：**{time_now}"
            },
            {
                "tag": "div",
                "fields": [
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": f"**服务名**\n{service_name}"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": f"**功能模块**\n{module_name}"
                        }
                    }
                ]
            }
        ]
    }

    SendFeishuCard(card)
