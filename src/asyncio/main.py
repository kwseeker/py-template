import asyncio
import os
import threading


def main():
    # 获取当前线程和主线程（主线程是解释器启动的线程）
    ct = threading.current_thread()
    mt = threading.main_thread()
    print(
        f"Current thread: {ct.name}, ident: {ct.ident}, Main thread: {mt.name}, ident: {mt.ident}")
    ac = threading.active_count()  # 获取当前活动线程数
    print(f"Active thread count: {ac}")
    pid = os.getpid()
    print(f"Current process ID: {pid}")

    # 获取当前运行的事件循环（_get_running_loop()），如果没有事件循环且当前为主线程，则按照获取事件循环的策略创建一个新的事件循环
    # 非主线程调用 get_event_loop() 如果当前没有事件循环，则会抛出错误，非主线程需要提前手动 new_event_loop() 创建事件循环
    # 事件循环被保存在 _RunningLoop 类实例的类属性（loop_pid）中, loop_pid 是一个元组
    #   _running_loop.loop_pid = (loop, os.getpid())
    # _RunningLoop 主要用于多进程，另外事件循环对象还会存储在线程的本地
    #   self._local._loop = loop
    # Python 事件循环基于单线程的IO多路复用模型实现
    # 看源码下面这两行代码和 asyncio.run(async_operation1()) 是等价的
    loop = asyncio.get_event_loop()
    loop.run_until_complete(async_operation1())

    # 创建事件循环并不会创建额外的线程，是在当前线程中进行协程调度的
    ac = threading.active_count()  # 获取当前活动线程数
    print(f"Active thread count: {ac}")

    # async def 定义的函数会返回一个协程对象, 协程对象个人理解其实是一个任务定义，交给 event loop 执行时通过 create_task() 转成了可调度的任务
    # 直接执行，会抛出警告：RuntimeWarning: coroutine 'async_operation1' was never awaited
    # 在 aiomysql 中看到的这段代码，其实不是执行协程，而是将协程对象进行了拓展，所以可以这么用
    #   def create_pool(minsize=1, maxsize=10, echo=False, pool_recycle=-1,
    #             loop=None, **kwargs):
    #         # _create_pool 是一个协程函数，返回一个协程对象
    #         coro = _create_pool(minsize=minsize, maxsize=maxsize, echo=echo,
    #                         pool_recycle=pool_recycle, loop=loop, **kwargs)
    #         return _PoolContextManager(coro)  # 接收一个线程对象
    # 应该放到事件循环中执行
    # async_operation1()
    asyncio.run(async_operation1())


async def async_operation1():
    print("Starting async_operation1")
    await async_operation2()
    print("Completed async_operation1")


async def async_operation2():
    print("Starting async_operation2")
    await asyncio.sleep(2)
    print("Completed async_operation2")

if __name__ == '__main__':
    main()
