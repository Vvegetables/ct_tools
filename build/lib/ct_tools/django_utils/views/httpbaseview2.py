from types import FunctionType
from django.conf.urls import url
from django.http.request import HttpRequest

class ClusterViewMeta(type):
    def __new__(cls, name:str, bases:tuple, attrs:dict):
        dispatch_func_list = []
        for key, value in attrs.items():
            if (isinstance(value, FunctionType)
                and
                not key.startswith("_") 
                ):
                dispatch_func_list.append(key)
        attrs["dispatch_func_list"] = dispatch_func_list
        return type.__new__(cls, name, bases, attrs)

class ClusterView(metaclass=ClusterViewMeta):
    
    prefix_url_path = None
    suffix_url_path = None
    
    @classmethod
    def as_view(cls, method):
        def _view(request:HttpRequest, *args, **kwargs):
            return getattr(cls(), method)(request, *args, **kwargs)
        return _view
    
    @classmethod
    def as_urls(cls, urlpatterns):
        for method in cls.dispatch_func_list:
            _method = method.replace("_", "-")
            _url_path_name = f"^{cls.prefix_url_path}-{_method}" if cls.prefix_url_path else f"^{_method}"
            _url_path_name = f"{_url_path_name}-{cls.suffix_url_path}/" if cls.suffix_url_path else f"{_url_path_name}/"
            
            urlpatterns.append(url(_url_path_name, cls.as_view(method)))