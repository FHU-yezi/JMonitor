from typing import Dict

from httpx import post as httpx_post

from config_manager import config
from utils import GetNowWithoutMileseconds


def GetFeishuToken() -> str:
    headers = {"Content-Type": "application/json; charset=utf-8"}
    data = {
        "app_id": config["message_sender/app_id"],
        "app_secret": config["message_sender/app_secret"]
    }
    response = httpx_post("https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal",
                          headers=headers, json=data)
    if response.json()["code"] == 0:
        return "Bearer " + response.json()["tenant_access_token"]
    else:
        raise ValueError(f"获取 Token 时发生错误，错误码：{response.json()['code']}，错误信息：{response.json()['msg']}")


def SendFeishuCard(card: Dict) -> None:
    token = GetFeishuToken()
    headers = {"Content-Type": "application/json; charset=utf-8",
               "Authorization": token}

    data = {
        "email": config["message_sender/email"],
        "msg_type": "interactive",
        "card": card
    }
    response = httpx_post("https://open.feishu.cn/open-apis/message/v4/send/",
                          headers=headers, json=data)
    if response.json()["code"] != 0:
        raise ValueError(f"发送消息卡片时发生错误，错误码：{response.json()['code']}，错误信息：{response.json()['msg']}")


def SendServiceUnavailableCard(service_name: str, module_name: str, status_code: int,
                               defined_error_name: str, error_message: str) -> None:
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
                            "content": f"**错误码**\n{status_code}"
                        }
                    },
                    {
                        "is_short": True,
                        "text": {
                            "tag": "lark_md",
                            "content": f"**错误名称**\n{defined_error_name}"
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
