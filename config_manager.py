from os import path as os_path

from yaml import SafeLoader
from yaml import dump as yaml_dump
from yaml import load as yaml_load

_DEFAULT_CONFIG = {
    "db_address": "localhost",
    "db_port": 27017,
    "minimum_record_log_level": "DEBUG",
    "minimum_print_log_level": "INFO",
    "message_sender": {
        "app_id": "",
        "app_secret": "",
        "email": ""
    }
}


class Config():
    def __new__(cls) -> "Config":
        # 单例模式
        if not hasattr(cls, "_instance"):
            cls._instance = object.__new__(cls)
        return cls._instance

    def __init__(self) -> None:
        if not os_path.exists("config.yaml"):  # 没有配置文件
            with open("config.yaml", "w", encoding="utf-8") as f:
                yaml_dump(_DEFAULT_CONFIG, f, allow_unicode=True, indent=4)
            self._config_dict = _DEFAULT_CONFIG
        else:  # 有配置文件
            with open("config.yaml", "r", encoding="utf-8") as f:
                self._config_dict = yaml_load(f, Loader=SafeLoader)

    def __getitem__(self, item):
        self.refresh()  # 刷新配置文件以应用更改
        item_path = item.split("/")
        result = self._config_dict
        for now_path in item_path:
            result = result[now_path]
        return result

    def refresh(self):
        self.__init__()


def InitConfig() -> Config:
    return Config()  # 初始化日志文件


config = InitConfig()
