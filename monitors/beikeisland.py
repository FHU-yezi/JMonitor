from helper import WebGetRequestHelper, WebPostRequestHelper
from register import MonitorFunc


@MonitorFunc("beikeisland", "website", "0 0/5 * * * *")
def beikeisland_website():
    return WebGetRequestHelper("https://www.beikeisland.com/index.html#/")


@MonitorFunc("beikeisland", "api", "0 0/5 * * * *")
def beikeisland_api():
    return WebPostRequestHelper("https://www.beikeisland.com/api/Trade/getTradeList",
                                data={"pageIndex": 1,
                                      "retype": 2
                                      })
