from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.utils.deprecation import MiddlewareMixin


__all__ = ['ProcessOptions']


class ProcessOptions(MiddlewareMixin):
    def process_request(self, request):
        if request.method == "OPTIONS":
            return HttpResponse()
    def process_exception(self, request:HttpRequest, exception):
        pass

#     def process_response(self, request:HttpRequest, response:HttpResponse):
#         pass
