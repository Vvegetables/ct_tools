from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils.deprecation import MiddlewareMixin


__all__ = ['ProcessOptions']


class ProcessOptions(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "OPTIONS":
            response = HttpResponse()
            try:
                response["Access-Control-Allow-Origin"] = request.META.get("HTTP_ORIGIN")
            except:
                response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "POST, GET, OPTIONS" 
            response["Access-Control-Max-Age"] = 1000 
            response["Access-Control-Allow-Headers"] = "*" 
            return response
    def process_exception(self, request:HttpRequest, exception):
        pass

#     def process_response(self, request:HttpRequest, response:HttpResponse):
#         pass
