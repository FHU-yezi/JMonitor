from helper import HTTP_get_request_helper
from register import monitor


@monitor("jianshu_micro_features", "website", "0 0/5 * * * *")
def jianshu_micro_features_website():
    return HTTP_get_request_helper("http://120.27.239.120:8602/")
