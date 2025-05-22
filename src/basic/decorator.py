"""装饰器
"""


from collections.abc import Callable
from functools import wraps
import time
from typing import Any


def decorate(func):
    """
    装饰器函数
    :param func: 被装饰的函数
    :return:
    """
    @wraps(func)  # 保留原函数的元数据
    def wrapper():
        print("开始执行装饰器")
        start_time = time.time()
        func()  # 执行被装饰的函数
        end_time = time.time()
        print("结束执行装饰器")
        print(f"执行时间: {end_time - start_time:.2f}秒")
    return wrapper


# 装饰器原理是将被装饰的函数作为参数传入装饰器函数，返回一个新的函数并绑定到原函数
# 下面代码相当于 biz_func = decorate(biz_func)
# 后面 @dec.tool() 装饰器的原则有点差别，是先执行 dec.tool() 返回一个新的函数，然后将 biz_func 作为参数传入这个新的函数
# 这个新的函数返回一个新的函数，最后将这个新的函数绑定到原函数
@decorate
def biz_func():
    print("业务逻辑处理")
    time.sleep(1)


class Decorator:

    def __init__(self):
        pass

    # def tool(self) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    #     # @wraps(func)  # 保留原函数的元数据
    #     def wrapper(fn: Callable[..., Any]) -> Callable[..., Any]:
    #         print("开始执行装饰器")
    #         start_time = time.time()
    #         fn()
    #         end_time = time.time()
    #         print("结束执行装饰器")
    #         print(f"执行时间: {end_time - start_time:.2f}秒")
    #         return fn
    #     return wrapper
    def tool(self):
        def wrapper(fn):
            @wraps(fn)
            def inner():
                print("开始执行装饰器")
                start_time = time.time()
                fn()
                end_time = time.time()
                print("结束执行装饰器")
                print(f"执行时间: {end_time - start_time:.2f}秒")
            return inner
        return wrapper


dec = Decorator()

# 这种装饰原理是先执行 dec.tool() 返回一个新的函数，然后将 biz_func 作为参数传入这个新的函数
# 这个新的函数返回一个新的函数，最后将这个新的函数绑定到原函数
# 所以这里装饰器中嵌套比前面的 @decorate 多了一层
# 相当于 biz_func2 = dec.tool()(biz_func2)


@dec.tool()
def biz_func2():
    print("业务逻辑处理2")
    time.sleep(1)


if __name__ == "__main__":
    # biz_func()
    biz_func2()
