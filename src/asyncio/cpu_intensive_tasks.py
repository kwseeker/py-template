"""
    asyncio 基于协作式调度，需要协程主动交出控制权（CPU资源），其他任务才能获取控制权并执行，
    不会像抢占式调度那样有时间片限制，
    如果所有任务整个流程都不会交出控制权，那么这些任务执行起来就是串行执行的，比如下面的 task1; 
    
    交出控制权的方式需要借助 await, 比如：
        await asyncio.sleep(0)
        await some_async_io_operation()
        await asyncio.yield()（Python 3.12+）
    
    asycio 并不适合处理CPU密集任务（CPU密集任务推荐使用线程池或进程池，使用多核计算）
    不过为了让多个CPU密集任务处理起来像是并发执行的，可以将任务拆分成多个小任务，
    小任务执行完毕后主动交出控制权，切换到执行其他任务的小任务，如 task2
"""

import asyncio
import time


async def task1(name):
    """这个任务没有主动交出控制权（CPU资源）所以会一直占用直到任务执行完成，其他任务才能执行, 导致看起来完全是串行执行
        A 开始: 1748966744.8917043
        A 结束: 1748966748.802334
        B 开始: 1748966748.802381
        B 结束: 1748966752.7223423
        C 开始: 1748966752.7223897
        C 结束: 1748966756.5353754
    """
    print(f"{name} 开始: {time.time()}")
    count = 0
    for _ in range(10**8):
        count += 1
    print(f"{name} 结束: {time.time()}")


async def task2(name):
    """这里改进一下，让3个CPU密集计算任务并发执行(看起来好像是在并行)
        A 开始: 1748966756.5355113
        B 开始: 1748966756.57786
        C 开始: 1748966756.619341
        A 结束: 1748966768.7790346
        B 结束: 1748966768.7790728
        C 结束: 1748966768.7790809
    """
    print(f"{name} 开始: {time.time()}")
    count = 0
    for _ in range(10**2):
        for _ in range(10**6):
            count += 1
        # 将CPU密集计算分成100个小片段，每执行完一个片段，手动释放控制权，去执行其他的任务片段
        await asyncio.sleep(0)
    print(f"{name} 结束: {time.time()}")


async def test():
    await asyncio.gather(task1("A"), task1("B"), task1("C"))
    print("---------------------------")
    await asyncio.gather(task2("A"), task2("B"), task2("C"))

if __name__ == "__main__":
    asyncio.run(test())
