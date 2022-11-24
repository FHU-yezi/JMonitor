from helper import WebGetRequestHelper
from register import MonitorFunc


@MonitorFunc("jianshu", "website", "0 1-59 * * * *")
def jianshu_website():
    return WebGetRequestHelper("https://www.jianshu.com")


@MonitorFunc("jianshu", "api", "0 1-59 * * * *")
def jianshu_api():
    return WebGetRequestHelper(
        "https://www.jianshu.com/asimov/users/slug/ea36c8d8aa30"
    )
