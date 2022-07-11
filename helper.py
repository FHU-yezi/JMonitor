from typing import Dict, Tuple

from httpx import ConnectTimeout, ReadTimeout
from httpx import get as httpx_get
from httpx import post as httpx_post

from code_to_desc import HTTPStatusCodeConvert


def WebGetRequestHelper(url: str, params: Dict = None,
                        headers: Dict = None) -> Tuple[bool, int, str]:
    if not params:
        params = {}
    if not headers:
        headers = {}

    try:
        response = httpx_get(url, timeout=3, params=params, headers=headers)
    except (ConnectTimeout, ReadTimeout):
        return (False, 2006, "")
    except Exception as e:
        return (False, 2000, repr(e))
    else:
        status_code = HTTPStatusCodeConvert(response.status_code)

    if status_code == 0:
        return (True, status_code, "")
    else:
        return (False, status_code, "")


def WebPostRequestHelper(url: str, data: Dict = None,
                         headers: Dict = None) -> Tuple[bool, int, str]:
    if not data:
        data = {}
    if not headers:
        headers = {}

    try:
        response = httpx_post(url, timeout=3, data=data, headers=headers)
    except (ConnectTimeout, ReadTimeout):
        return (False, 2006, "")
    except Exception as e:
        return (False, 2000, repr(e))
    else:
        status_code = HTTPStatusCodeConvert(response.status_code)

    if status_code == 0:
        return (True, status_code, "")
    else:
        return (False, status_code, "")
