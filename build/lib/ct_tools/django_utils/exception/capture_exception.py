#coding=utf-8
import traceback
from io import StringIO
from functools import wraps

#捕获最后的异常
def cap_exception(return_func=None):
    def out_wraps(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            try:
                return func(request, *args, **kwargs)
            except Exception as e:
                #测试
                print(e)
                fp = StringIO()
                traceback.print_exc(file=fp)
                msg = fp.getvalue()
                with open("error.log", "a+", encoding="utf-8") as f:
                    f.write(msg)
                return return_func if not return_func else return_func()

        return wrapper

    return out_wraps
