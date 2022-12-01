from helper import HTTP_get_request_helper, HTTP_post_request_helper
from register import monitor


@monitor("beikeisland", "website", "0 0/5 * * * *")
def beikeisland_website():
    return HTTP_get_request_helper("https://www.beikeisland.com/index.html#/")


@monitor("beikeisland", "api", "0 0/5 * * * *")
def beikeisland_api():
    return HTTP_post_request_helper(
        "https://www.beikeisland.com/api/Trade/getTradeList",
        data={"pageIndex": 1, "retype": 2}
    )
