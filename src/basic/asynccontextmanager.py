""" @asynccontextmanager
@asynccontextmanager 是 Python 的 contextlib 模块提供的装饰器，用于简化异步上下文管理器（Async Context Manager）的创建
可以将异步生成器函数转换为异步上下文管理器, 即将 async ... yield ... 转换为可以被 async with 调用的实现了 __aenter__ __aexit__ 的异步上下文管理器
注意只能用于异步生成器。

原理：
装饰器会将生成器函数转换为一个实现了 __aenter__ 和 __aexit__ 的类：
__aenter__：驱动生成器执行到 yield，返回产出的值。
__aexit__：继续执行生成器剩余的代码（清理逻辑）。
"""

from contextlib import asynccontextmanager
import asyncio


@asynccontextmanager
async def async_resource_manager():
    # 此处模拟异步资源初始化（相当于 __aenter__）
    print("Resource initialized")
    yield "resource_handle"  # 资源对象会传递给 asyn with 的变量
    # 此处模拟异步资源清理（相当于 __aexit__）
    print("Resource cleaned up")


async def main():
    async with async_resource_manager() as resource:
        print(f"Using resource: {resource}")

# 等价于

# class AsyncResourceManager:
#     async def __aenter__(self):
#         print("Resource initialized")
#         return "resource_handle"

#     async def __aexit__(self, exc_type, exc_val, exc_tb):
#         print("Resource cleaned up")

# async def main():
#     async with AsyncResourceManager() as resource:
#         print(f"Using resource: {resource}")

asyncio.run(main())

# --------------------------------------------


@asynccontextmanager
async def temp_file_handler():
    path = "/tmp/async_temp.txt"
    with open(path, "w") as f:
        f.write("test")
    try:
        yield path
    finally:
        import os
        os.remove(path)


async def process_file():
    async with temp_file_handler() as file_path:
        print(f"Processing file: {file_path}")

asyncio.run(process_file())
