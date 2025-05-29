import asyncio
import collections


class Pool:
    """连接池

    工作原理：
    1. 获取连接


    正确关闭连接池的方法：
    1. 优雅关闭： 先调用 close() 方法然后等待关闭完成 wait_closed()
    2. 立即关闭： 先调用 terminate() 方法然后等待关闭完成 wait_closed()
    """

    def __init__(self, minsize, maxsize, echo, pool_recycle, loop, **kwargs):
        if minsize < 0:
            raise ValueError("minsize should be zero or greater")
        if maxsize < minsize and maxsize != 0:
            raise ValueError("maxsize should be not less than minsize")
        # 连接池维持最小连接数
        self._minsize = minsize
        self._loop = loop
        self._conn_kwargs = kwargs
        # 空闲连接的双端队列， maxsize or None 的意思是 maxsize 为"真值"取maxsize 否则取 None
        self._free = collections.deque(maxlen=maxsize or None)
        # 已经创建并被使用的连接
        self._used = set()
        # 已终止的连接，终止连接池才会用到
        self._terminated = set()
        # 这个异步条件变量
        self._cond = asyncio.Condition()
        self._echo = echo
        self._recycle = pool_recycle
        # 四种状态
        self._acquiring = 0

        # 是否正在关闭连接池
        self._closing = False
        # 连接池是否已经关闭完成
        self._closed = False

    @property
    def echo(self):
        return self._echo

    @property
    def minsize(self):
        return self._minsize

    @property
    def maxsize(self):
        return self._free.maxlen

    @property
    def size(self):
        return self.freesize + len(self._used) + self._acquiring

    @property
    def freesize(self):
        return len(self._free)

    async def clear(self):
        """清理连接池中所有的空闲连接"""
        async with self._cond:      # 这一行的作用从其异步上下文管理器的定义看就是先获取锁，然后执行代码块，最后释放锁，即线程安全地执行代码块
            while self._free:
                conn = self._free.popleft()
                await conn.ensure_closed()
            # TODO 为什么
            self._cond.notify()

    @property
    def closed(self):
        """当所有的连接都关闭后返回 True"""
        return self._closed

    def close(self):
        """关闭连接池，其实是优雅关闭线程池
        仅仅设置关闭中的状态，并不会立即关闭正在使用的连接，关闭连接池后续回收的连接会被关闭
        拒绝获取新连接
        需要配合 wait_closed() 使用
        """
        if self._closed:
            return
        self._closing = True

    def terminate(self):
        """立即终止连接池，其实是立即终止使用中的连接
        会立即关闭所有的连接（包括使用中的）
        需要配合 wait_closed() 使用
        """
        self.close()
        for conn in list(self._used):
            conn.close()
            self._terminated.add(conn)
        # 为何只清除 _used ? _free 不清除？因为 _free 被清除是借助 wait_closed() 方法实现 ，
        # 也即 terminate() 也需要配合 wait_closed() 使用
        self._used.clear()

    async def wait_closed(self):
        """Wait for closing all pool's connections."""

        if self._closed:
            return
        if not self._closing:
            raise RuntimeError(".wait_closed() should be called "
                               "after .close()")

        while self._free:
            conn = self._free.popleft()
            conn.close()

        async with self._cond:
            while self.size > self.freesize:    # 即有正在使用的连接，需要等待这些连接任务执行完成
                await self._cond.wait()

        self._closed = True

    def acquire(self):
        """从连接池获取连接并在使用完连接后自动恢复到连接池
        """
        coro = self._acquire()
        return _PoolAcquireContextManager(coro, self)

    async def _acquire(self):
        """从连接池获取连接       
        如果 _free 中有空闲连接，直接从 _free 获取连接
        _free 中没有空闲连接则等待 _fill_free_pool() 协程创建并插入空闲连接
        """
        if self._closing:
            raise RuntimeError("Cannot acquire connection after closing pool")
        async with self._cond:
            while True:
                await self._fill_free_pool(True)
                if self._free:
                    conn = self._free.popleft()     #
                    assert not conn.closed, conn
                    assert conn not in self._used, (conn, self._used)
                    self._used.add(conn)
                    return conn
                else:
                    await self._cond.wait()

    async def _fill_free_pool(self, override_min):
        # iterate over free connections and remove timed out ones
        free_size = len(self._free)
        n = 0
        while n < free_size:
            conn = self._free[-1]
            if conn._reader.at_eof() or conn._reader.exception():
                self._free.pop()
                conn.close()

            # On MySQL 8.0 a timed out connection sends an error packet before
            # closing the connection, preventing us from relying on at_eof().
            # This relies on our custom StreamReader, as eof_received is not
            # present in asyncio.StreamReader.
            elif conn._reader.eof_received:
                self._free.pop()
                conn.close()

            elif (self._recycle > -1 and
                  self._loop.time() - conn.last_usage > self._recycle):
                self._free.pop()
                conn.close()

            else:
                self._free.rotate()
            n += 1

        while self.size < self.minsize:
            self._acquiring += 1
            try:
                conn = await connect(echo=self._echo, loop=self._loop,
                                     **self._conn_kwargs)
                # raise exception if pool is closing
                self._free.append(conn)
                self._cond.notify()
            finally:
                self._acquiring -= 1
        if self._free:
            return

        if override_min and (not self.maxsize or self.size < self.maxsize):
            self._acquiring += 1
            try:
                conn = await connect(echo=self._echo, loop=self._loop,
                                     **self._conn_kwargs)
                # raise exception if pool is closing
                self._free.append(conn)
                self._cond.notify()
            finally:
                self._acquiring -= 1

    async def _wakeup(self):
        async with self._cond:
            self._cond.notify()

    def release(self, conn):
        """Release free connection back to the connection pool.

        This is **NOT** a coroutine.
        """
        fut = self._loop.create_future()
        fut.set_result(None)

        if conn in self._terminated:
            assert conn.closed, conn
            self._terminated.remove(conn)
            return fut
        assert conn in self._used, (conn, self._used)
        self._used.remove(conn)
        if not conn.closed:
            in_trans = conn.get_transaction_status()
            if in_trans:
                conn.close()
                return fut
            if self._closing:
                conn.close()
            else:
                self._free.append(conn)
            fut = self._loop.create_task(self._wakeup())
        return fut

    def __enter__(self):
        raise RuntimeError(
            '"yield from" should be used as context manager expression')

    def __exit__(self, *args):
        # This must exist because __enter__ exists, even though that
        # always raises; that's how the with-statement works.
        pass  # pragma: nocover

    def __iter__(self):
        # This is not a coroutine.  It is meant to enable the idiom:
        #
        #     with (yield from pool) as conn:
        #         <block>
        #
        # as an alternative to:
        #
        #     conn = yield from pool.acquire()
        #     try:
        #         <block>
        #     finally:
        #         conn.release()
        conn = yield from self.acquire()
        return _PoolConnectionContextManager(self, conn)

    # def __await__(self):
    #     """
    #     用于定义一个对象的异步迭代行为，使其能够用于 await 表达式
    #     当你自定义一个类，并希望它能像协程一样被 await 使用时，就需要实现 __await__ 方法
    #     """
    #     msg = "with await pool as conn deprecated, use" \
    #           "async with pool.acquire() as conn instead"
    #     warnings.warn(msg, DeprecationWarning, stacklevel=2)
    #     conn = yield from self.acquire()
    #     return _PoolConnectionContextManager(self, conn)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()
        await self.wait_closed()
