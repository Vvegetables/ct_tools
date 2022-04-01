from functools import wraps
import time

# 函数运行时间打印
def func_runtime_print_decorator(is_print: bool=True):
	def args_wrapper(func):
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