import json
from _io import BytesIO
import os
from types import FunctionType

from django.conf.urls import url
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils.encoding import escape_uri_path
from typing import Tuple


class ClusterViewMeta(type):
    def __new__(mcs, name:str, bases:tuple, attrs:dict):
        dispatch_func_list = []
        for key, value in attrs.items():
            if (isinstance(value, (FunctionType, staticmethod, classmethod))
                and
                not key.startswith("_") 
                ):
                dispatch_func_list.append(key)
        attrs["dispatch_func_list"] = dispatch_func_list
        return type.__new__(mcs, name, bases, attrs)

class ClusterView(metaclass=ClusterViewMeta):
    
    prefix_url_path = None
    suffix_url_path = None
    
    def __init__(self, request=None):
        if request:
            self.request = request

    # 获得分页
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
        def _view(request:HttpRequest, *args, **kwargs):
            return getattr(cls(request), method)(request, *args, **kwargs)
        return _view
    
    @classmethod
    def as_urls(cls, urlpatterns):
        for method in cls.dispatch_func_list:
            _method = method.replace("_", "-")
            _url_path_name = f"^{cls.prefix_url_path}-{_method}" if cls.prefix_url_path else f"^{_method}"
            _url_path_name = f"{_url_path_name}-{cls.suffix_url_path}/" if cls.suffix_url_path else f"{_url_path_name}/"
            
            urlpatterns.append(url(_url_path_name, cls.as_view(method)))
    
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