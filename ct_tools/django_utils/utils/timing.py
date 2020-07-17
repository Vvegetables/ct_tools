from functools import wraps
import time

# 函数运行时间打印
def _func_runtime_print_decorator(func):
	def args_wrapper(is_print: bool=False)
	    @wraps(func)
	    def wrapper(*args, **kwargs):
	        start_time_ = time.time()
	        result = func(*args, **kwargs)
	        end_time_ = time.time()
	        if is_print:
	            print(f"{func.__name__}消耗时间: {end_time_ - start_time_}")
	        return result
	    return wrapper
	return args_wrapper