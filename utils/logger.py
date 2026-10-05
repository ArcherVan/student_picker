from functools import wraps
def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print("开始执行", func.__name__)
        try:
            result = func(*args, **kwargs)
            print("日志打印结束")
            return result
        except Exception as e:
            print(f"发生异常: {e}")
            raise
    return wrapper

