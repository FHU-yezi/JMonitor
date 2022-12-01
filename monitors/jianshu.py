from helper import HTTP_get_request_helper
from register import monitor


@monitor("jianshu", "website", "0 1-59 * * * *")
def jianshu_website():
    return HTTP_get_request_helper("https://www.jianshu.com")


@monitor("jianshu", "api", "0 1-59 * * * *")
def jianshu_api():
    return HTTP_get_request_helper(
        "https://www.jianshu.com/asimov/users/slug/ea36c8d8aa30"
    )
