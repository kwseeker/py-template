import asyncio
from .utils import _ConnectionContextManager


class Conn:

    count = 0
    lock = asyncio.Lock()

    async def __init__(self):
        async with Conn.lock:
            Conn.count += 1
            self.id = Conn.count
        self.closed = False

    @classmethod
    async def create(cls):
        self = cls.__new__(cls)
        await self.__init__()
        return self

    def info(self):
        return self.id

    def close(self):
        """关闭连接，关闭连接池或关闭最小连接数外长期空闲的连接时才会调用"""
        self.closed = True
        print(f"Connection {self.id} closed")

    async def ensure_closed(self):
        print(
            f"Connection {self.id}: waiting ack after send quit command to close...")
        await asyncio.sleep(1)
        self.close()

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:        # 如果出现异常，直接关闭连接
            self.close()
        else:               # 没有异常，先发送关闭命令再关闭连接
            await self.ensure_closed()
        return


def connect():
    coro = _connect()
    return _ConnectionContextManager(coro)


async def _connect():
    conn = await Conn.create()
    print(f"created new conn, id: {conn.id}")
    return conn
