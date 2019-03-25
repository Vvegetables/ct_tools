from io import StringIO
import logging
from traceback import print_exc
from django.utils.deprecation import MiddlewareMixin
from ..responses import ct_response
import datetime


__all__ = ['ExceptionRecordMiddleware']

class ExceptionRecordMiddleware(MiddlewareMixin):
    def process_exception(self, request, exception):
        fp = StringIO()
        print_exc(file=fp)
        msg = fp.getvalue()
        fp.close()
        with open("error.log", "a+", encoding="utf-8") as f:
            f.write(format_logging_msg(str(datetime.datetime.now()), request.path, msg))
        response = ct_response("系统错误", 1)
        return response

def format_logging_msg(_time, path, exception):
    msg = f"""
##########
time: {_time}
path: {path}
exception:
{exception}
##########
"""
    return msg
