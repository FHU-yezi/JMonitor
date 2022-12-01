from helper import HTTP_get_request_helper
from register import monitor


@monitor("jianshu_micro_features", "website", "0 0/5 * * * *")
def jianshu_micro_features_website():
    return HTTP_get_request_helper("http://120.27.239.120:8602/")


@monitor("wind_with_2021", "website", "0 0/5 * * * *")
def wind_with_2021_website():
    return HTTP_get_request_helper("http://120.27.239.120:8603")
