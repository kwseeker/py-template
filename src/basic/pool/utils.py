from typing import Coroutine


class _ContextManager(Coroutine):
    """ 
    实现 __aenter__ __aexit__ 支持 async with 语义
    协程的 send throw close __await__方法的作用：
        send(): 开始或恢复协程的执行
        throw(): 在协程内引发指定的异常
        close(): 使得协程清理自身并退出
        __await__(): 
    """

    __slots__ = ('_coro', '_obj')

    def __init__(self, coro):
        self._coro = coro
        # _obj 接收 async with 表达式的返回值
        self._obj = None

    def send(self, value):
        return self._coro.send(value)

    def throw(self, typ, val=None, tb=None):
        if val is None:
            return self._coro.throw(typ)
        elif tb is None:
            return self._coro.throw(typ, val)
        else:
            return self._coro.throw(typ, val, tb)

    def close(self):
        return self._coro.close()

    @property
    def gi_frame(self):
        """当前协程正在执行的栈帧（frame）"""
        return self._coro.gi_frame

    @property
    def gi_running(self):
        """协程是否正在运行"""
        return self._coro.gi_running

    @property
    def gi_code(self):
        """协程对应的代码对象"""
        return self._coro.gi_code

    def __next__(self):
        """返回"""
        return self.send(None)

    def __iter__(self):
        """返回迭代器对象，这里返回会返回协程事件的生成器"""
        return self._coro.__await__()

    def __await__(self):
        """允许对象被 await, 表明这是一个 awaitable 对象，这里返回会返回协程事件的生成器"""
        return self._coro.__await__()

    async def __aenter__(self):
        """等待协程执行完成，返回值保存到 _obj, 这里是 Conn"""
        self._obj = await self._coro
        return self._obj

    async def __aexit__(self, exc_type, exc, tb):
        """这里是释放 Conn"""
        await self._obj.close()
        self._obj = None


class _PoolAcquireContextManager(_ContextManager):

    # 显式声明类中使用的属性名列表
    #   减少内存占用；
    #   提高访问速度；
    #   禁止动态添加未声明的属性。
    __slots__ = ('_coro', '_conn', '_pool')

    def __init__(self, coro, pool):
        self._coro = coro
        self._conn = None
        self._pool = pool

    async def __aenter__(self):
        self._conn = await self._coro
        return self._conn

    async def __aexit__(self, exc_type, exc, tb):
        try:
            await self._pool.release(self._conn)
        finally:
            self._pool = None
            self._conn = None


class _PoolConnectionContextManager:
    """Context manager.

    This enables the following idiom for acquiring and releasing a
    connection around a block:

        with (yield from pool) as conn:
            cur = yield from conn.cursor()

    while failing loudly when accidentally using:

        with pool:
            <block>
    """

    __slots__ = ('_pool', '_conn')

    def __init__(self, pool, conn):
        self._pool = pool
        self._conn = conn

    def __enter__(self):
        assert self._conn
        return self._conn

    def __exit__(self, exc_type, exc_val, exc_tb):
        try:
            self._pool.release(self._conn)
        finally:
            self._pool = None
            self._conn = None

    async def __aenter__(self):
        assert not self._conn
        self._conn = await self._pool.acquire()
        return self._conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            await self._pool.release(self._conn)
        finally:
            self._pool = None
            self._conn = None


class _ConnectionContextManager(_ContextManager):
    async def __aexit__(self, exc_type, exc, tb):
        if exc_type is not None:
            self._obj.close()
        else:
            await self._obj.ensure_closed()
        self._obj = None
