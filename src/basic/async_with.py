"""async with 语句

    async with 后面的表达式的返回值类型需要实现 __aenter__ __aexit__ 方法

    这里参考 aiomysql 中的连接池实现，测试 async with
"""

from contextlib import asynccontextmanager

from basic.pool.conn import Conn

# async def 函数实际会返回一个协程，这里的协程执行（比如await 、async with）返回 Conn
# asynccontextmanager 装饰器用于修饰 async 生成器(yield返回值)


@asynccontextmanager
async def get_conn() -> Conn:
    yield Conn()


async def main():
    async with get_conn() as conn:
        print("使用连接执行业务操作")
        pass

main()
