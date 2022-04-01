import functools
import inspect
import json
import typing
from _io import BytesIO
import os
from types import FunctionType

from django.conf.urls import url
from django.http.request import HttpRequest, QueryDict, MultiValueDict
from django.http.response import HttpResponse
from django.utils.encoding import escape_uri_path
from typing import Tuple


# 不在url中显示
def exclude(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)

    wrapper.exclude = True
    return wrapper


def add_method(key: str, value: typing.Any, container: typing.List):
    # staticmethod classmethod
    if (isinstance(value, (FunctionType, ))
            and not key.startswith("_")
            and not getattr(value, "exclude", False)
            and key not in container
    ):
        container.append(key)


def extend_method(method_list: typing.List[str], container: typing.List):
    for m in method_list:
        if m not in container:
            container.append(m)


class ClusterViewMeta(type):
    def __new__(mcs, name: str, bases: tuple, attrs: dict):

        dispatch_func_list = []

        for base in bases:
            for key, n in base.__dict__.items():
                add_method(key, n, dispatch_func_list)

            extend_method(getattr(base, "dispatch_func_list", []),
                          dispatch_func_list)

        for key, value in attrs.items():
            add_method(key, value, dispatch_func_list)

        attrs["dispatch_func_list"] = dispatch_func_list
        return type.__new__(mcs, name, bases, attrs)


class ClusterView(metaclass=ClusterViewMeta):
    prefix_url_path = None
    suffix_url_path = None

    def __init__(self, request=None):
        if request:
            self.request = request

    def _get_params(self):
        if self.request.content_type == "application/json":
            param = json.loads(self.request.body)
        elif self.request.content_type in [
            "multipart/form-data",
            "application/x-www-form-urlencoded",
            "text/html"
        ]:
            param = self.request.POST.dict() or self.request.GET.dict()
        else:
            param = {}

        return param

    # 获得分页
    @exclude
    def pagination(self, request: HttpRequest) -> Tuple[int, int]:
        if "application/json" in request.content_type:
            try:
                req = json.loads(request.body)
            except:
                req = {}
        else:
            req = request.POST or request.GET

        page_no = req.get("pageNo", 1)
        page_size = req.get("pageSize", 20)

        return (page_no - 1) * page_size, page_no * page_size

    @classmethod
    def as_view(cls, method):
        func_ = getattr(cls, method)

        @functools.wraps(func_)
        def _view(request: HttpRequest, *args, **kwargs):
            return getattr(cls(request, *args, **kwargs), method)(request, *args, **kwargs)

        return _view

    @classmethod
    def as_urls(cls, urlpatterns):
        for method in cls.dispatch_func_list:
            _view = cls.as_view(method)

            if not getattr(_view, "exclude", False):
                _method = method.replace("_", "-")
                _url_path_name = f"^{cls.prefix_url_path}-{_method}" if cls.prefix_url_path else f"^{_method}"
                _url_path_name = f"{_url_path_name}-{cls.suffix_url_path}/" if cls.suffix_url_path else f"{_url_path_name}/"
                urlpatterns.append(url(_url_path_name, _view, name=inspect.getdoc(_view)))

    @staticmethod
    def excel_download(workbook, filename, DEBUG=True, BASE_DIR=None):
        if DEBUG and BASE_DIR:
            dir_name = os.path.join(BASE_DIR, "static", "export")
            full_path = os.path.join(dir_name, filename)
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            workbook.save(full_path)
            response = HttpResponse()
            return response
        else:
            filename = escape_uri_path(filename)
            with BytesIO() as x_io:
                workbook.save(x_io)
                response = HttpResponse(x_io.getbuffer())
                response["Content-Type"] = "application/octet-stream"
                response['Access-Control-Allow-Credentials'] = "true"
                response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
                response["Content-Disposition"] = f"attachment; filename={filename}"
            return response
