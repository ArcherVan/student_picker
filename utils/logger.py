def log(func):
    def wrapper(*args, **kwargs):
        print("开始执行",func.__name__)
        result = func(*args, **kwargs)
        print("日志打印结束")
        return result
    return wrapper

