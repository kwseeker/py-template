"""asyncio Condition
    和 Java 中锁的 Condition 类似
    
    只有获得内部锁后，才能进入 async with 块。
    协程可以调用 wait() 暂停执行（条件不满足等待），直到其他协程调用 notify() 来唤醒它（条件满足唤醒）。
    
    场景：
    1. 资源池（如连接池）
    2. 生产者-消费者模型
    3. 限流器 / 信号量控制
    
    Python 实现并发的三种方式：
    1. 多进程
    2. 多线程
    3. asyncio
"""

import asyncio

count = 0
count2 = 0

cond = asyncio.Condition()


async def incr():
    global count
    i = 0
    while i < 100:
        c = count
        # 模拟处理延迟，从 asyncio 调度看感觉没有时间片的概念，看上去只有当某个任务执行完成或者进入等待状态后才会让出计算资源
        # 因为从打印结果看比较固定，不像 Java 这种有线程安全问题的代码打印数值很随机
        # TODO 源码分析
        await asyncio.sleep(0.1)
        count = c + 1
        i += 1


async def incr_safe():
    global count2
    i = 0
    while i < 100:
        async with cond:    # 先获取锁，最后释放锁；只需要用到锁，这个例子不太适合测试 Condition, 这里 async with 会调用 _ContextManagerMixin 中的 __aenter__() 这方法中用于获取锁
            c = count2
            await asyncio.sleep(0.1)
            count2 = c + 1
            i += 1


async def main():   # 三个任务并发执行
    await asyncio.gather(incr(), incr(), incr())
    await asyncio.gather(incr_safe(), incr_safe(), incr_safe())

asyncio.run(main())

print(count)    # 100
print(count2)   # 300
