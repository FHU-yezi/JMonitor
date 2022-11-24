from helper import WebGetRequestHelper
from register import MonitorFunc


@MonitorFunc("jianshu_micro_features", "website", "0 0/5 * * * *")
def jianshu_micro_features_website():
    return WebGetRequestHelper("http://120.27.239.120:8602/")


@MonitorFunc("wind_with_2021", "website", "0 0/5 * * * *")
def wind_with_2021_website():
    return WebGetRequestHelper("http://120.27.239.120:8603")
