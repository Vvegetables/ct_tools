import json
import os
import datetime
from io import BytesIO

from django.conf.urls import url
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils.encoding import escape_uri_path
from openpyxl.reader.excel import load_workbook
from openpyxl.workbook.workbook import Workbook

class HBViewMeta(type):
    def __new__(cls, classname, extends_tuple, attr_dict):
        must_argv = ("url_path", )
        for argv in must_argv:
            if argv not in attr_dict:
                raise ValueError('url_path must be defined')
        url_path = attr_dict.get("url_path")
        if url_path:
            attr_dict["url_path"] = f'{url_path}/' if not url_path.endswith("/") else url_path
        return super().__new__(cls, classname, extends_tuple, attr_dict)


class HttpBaseView(metaclass=HBViewMeta):
    def get_json_params(self, request):
        try:
            reqall = request.POST
            setattr(request, "reqall", reqall)
        except Exception as e:
            pass
    
    methods = ["search"]
    url_path = "api"
    handle_request_before_view = ["get_json_params"]
    
    @classmethod
    def dispatch(cls, method, request, *args, **kwargs):
        self = cls()
        obj_method = getattr(self, method)
        for handle in cls.handle_request_before_view:
            getattr(self, handle)(request)
        
        return obj_method(request, *args, **kwargs)
    
    @classmethod
    def as_view(cls, method):
        def _view(request:HttpRequest, *args, **kwargs):
            return cls.dispatch(method, request, *args, **kwargs)
        return _view
    
    @classmethod
    def as_urls(cls, urlpatterns):
        for method in cls.methods:
            url_path_name = f"^{cls.url_path}-{method}/"
            urlpatterns.append(url(url_path_name, cls.as_view(method)))
    
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
                response['Access-Control-Allow-Credentials'] = True
                response['Access-Control-Allow-Methods'] = 'POST, GET, OPTIONS'
                response["Content-Disposition"] = f"attachment; filename={filename}"
            return response