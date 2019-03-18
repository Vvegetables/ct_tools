import logging
from io import StringIO
from traceback import print_exc
from ..responses import ct_response

__all__ = ['ExceptionRecordMiddleware']

class ExceptionRecordMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        response = self.get_response(request)
        return response
    
    def poccess_exception(self, request, exception):
        fp = StringIO()
        print_exc(file=fp)
        msg = fp.getvalue()
        fp.close()
        with open("error.log", "a+", encoding="utf-8") as f:
            f.write(format_logging_msg(request.path, msg))
        response = ct_response("系統錯誤", 1)
        return response


def format_logging_msg(path, exception):
    msg = f"""
        ##########\n
        path: {path}\n
        exception: \n
        {exception}
        ##########\n
        """
    return msg
