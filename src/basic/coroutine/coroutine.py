"""协程对象
    https://docs.python.org/zh-cn/3.13/reference/datamodel.html#coroutine-objects
    https://docs.python.org/3/library/asyncio-task.html
    
    协程对象特征：
        是可等待的（awaitable），可以被 await；
        支持 .send(), .throw(), .close() 方法；
        可以通过调用 __await__() 获取其底层迭代器；
        不直接支持 for 循环（即不能直接用于迭代）；
        
    send() 方法：
        用于向协程发送一个值，并且这个值会成为当前挂起的 yield 表达式的返回值。
        这对于实现双向通信非常有用，比如在一个协程中等待外部输入来决定后续的操作流程。
    throw() 方法：
        允许你在协程内部引发异常。这可以用于模拟错误处理或测试协程如何应对异常情况。
        当调用 throw() 时，异常会在最近一次挂起的 yield 位置被抛出。
    close() 方法：
        用于关闭协程，清理资源。这会触发 GeneratorExit 异常，如果协程没有捕获并处理这个异常，则会立即终止执行。
        
    在异步编程中，尽量使用 await 而不是手动调用 send() / throw()
    除非想要理解其底层机制或编写高级库。
"""

# 协程模拟实现

counter = 0


class WaitB:
    def __await__(self):
        yield "B"


class WaitC:
    def __await__(self):
        yield "C"


async def coroutine():
    global counter
    id = counter
    counter += 1

    print(f"{id} Processing event A, blocking on B")
    await WaitB()
    print(f"{id} Processing event B, blocking on C")
    await WaitC()
    print(f"{id} Processing event C, task done")


def app():
    # 等待某事件的任务队列，这里的 coroutine 任务先后等待 B C
    tasks = {"A": [], "B": [], "C": []}
    while True:																	# while 模拟 event loop
        print(f"Task queue size {len(tasks['A'] + tasks['B'] + tasks['C'])}")
        event = input("> ").strip()												# 模拟监听到就绪事件

        if event == "A":
            new_task = coroutine()					# 创建外部任务协程
            # 启动协程，send() 返回挂起的第一个 yield 表达式的值，最初是 "B"
            waiting_for = new_task.send(None)
            tasks[waiting_for].append(new_task)		# 记录 new_task 等待 B 事件
            # 然后会启动 WaitB 异步迭代（可以想像这里WaitB是另一个协程），完成后会返回B事件，下一轮事件循环会读取到B事件

        if len(tasks[event]):			# 第2轮事件循环会读取到 B事件
            task = tasks[event][0]		# 获取等待B事件的协程
            tasks[event].remove(task)
            try:
                waiting_for = task.send(None)  # 恢复之前挂起的协程
                # 发现还会等待 C 事件，再将协程放入等待C事件的任务队列，等待C事件就绪后处理
                tasks[waiting_for].append(task)
            except StopIteration:
                pass


if __name__ == "__main__":
    app()
