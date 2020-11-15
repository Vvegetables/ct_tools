from django.http import HttpRequest
from typing import Optional


# 从request上获得ip地址
def get_ip(request: HttpRequest):
    if request.META.get('HTTP_X_FORWARDED_FOR'):
        ip = request.META.get("HTTP_X_FORWARDED_FOR")
    else:
        ip = request.META.get("REMOTE_ADDR")

    return ip

# 用于装饰器《查找request》
def find_request(*args, **kwargs) -> Optional[HttpRequest]:
    if len(args) >= 1:
        if hasattr(args[0], "get_host"):
            return args[0]
    if len(args) >= 2:
        if hasattr(args[1], "get_host"):
            return args[1]
    if kwargs.get("request"):
        return kwargs["request"]