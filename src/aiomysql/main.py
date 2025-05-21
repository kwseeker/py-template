""" aiomysql
    文档: https://aiomysql.readthedocs.io/en/latest/index.html
"""

import asyncio
import aiomysql


class MySQLConnManager:
    def __init__(self, host, port, user, password, db):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.db = db
        self.pool = None

    async def init_pool(self):
        # 创建连接池
        if self.pool is None:
            self.pool = await aiomysql.create_pool(host=self.host, port=self.port,
                                                   user=self.user, password=self.password,
                                                   db=self.db)

    async def acquire_conn(self):
        # 从连接池中获取连接
        if self.pool is None:
            await self.init_pool()
        conn = await self.pool.acquire()
        return conn

    def release_conn(self, conn):
        # 释放连接恢复到连接池
        if conn is not None and self.pool is not None:
            self.pool.release(conn)

    async def close(self):
        if self.pool is not None:
            self.pool.close()
            await self.pool.wait_closed()
            self.pool = None


def main():
    asyncio.run(query())


async def query():
    conn_manager = MySQLConnManager(host='192.168.8.100', port=3306,
                                    user='root', password='123456',
                                    db='employees')
    conn = await conn_manager.acquire_conn()
    # async with 是一种语法糖，需要定义上下文管理器类，定义 __aenter__ 和 __aexit__ 方法，分别用于方法开始和结束时的操作
    # 比如 aiomysql 中的 _PoolAcquireContextManager 类, 定义了从连接池中获取连接前和获取后（包括异常处理）的操作
    #   def acquire(self):
    #       """Acquire free connection from the pool."""
    #       coro = self._acquire()
    #       return _PoolAcquireContextManager(coro, self)
    async with conn.cursor() as cur:
        # await cur.execute("SELECT 10")
        await cur.execute("select * from employees where emp_no = '10001';")
        print(cur.description)
        # (r,) = await cur.fetchone()
        # assert r == 10

    print("query done")

if __name__ == '__main__':
    main()
