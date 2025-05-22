"""
https://docs.python.org/3/library/asyncio-eventloop.html
get_event_loop() 用于获取线程事件循环对象，对于主线程来说如果事件循环不存在会主动创建并调用 set_event_loop 存储到主线程线程本地
非主线程直接调用 get_event_loop() 会抛出错误，需要先 new_event_loop 后 set_event_loop 然后才能 get_event_loop()
一个线程却可以创建多个事件循环，只不过只有通过 set_event_loop() 事件循环对象才会存储到线程的线程本地
被关闭的事件循环对象不能再启用，关闭后再次调用 get_event_loop() 会返回同一个事件循环对象
"""

import asyncio
import threading


async def hello():
    print("Hello, world!")
    await asyncio.sleep(1)


def thread_function(name):
    print(f"线程 {name} 开始")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop1 = asyncio.get_event_loop()
    loop1.run_until_complete(hello())
    loop2 = asyncio.new_event_loop()
    print(f"New event loop: {loop}, id: {id(loop)}")
    print(f"New event loop: {loop1}, id: {id(loop1)}")
    print(f"New event loop: {loop2}, id: {id(loop2)}")
    print(f"线程 {name} 结束")


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    print(f"Current event loop: {loop}, id: {id(loop)}")
    loop.close()
    # 关闭之后再获取还是同一个事件循环
    loop = asyncio.get_event_loop()
    print(f"Current event loop: {loop}, id: {id(loop)}")
    # 线程可以创建多个事件循环对象
    new_loop = asyncio.new_event_loop()
    new_loop.run_until_complete(hello())
    print(f"New event loop: {new_loop}, id: {id(new_loop)}")
    loop = asyncio.set_event_loop(new_loop)
    loop2 = asyncio.get_event_loop()
    print(f"Current event loop: {loop2}, id: {id(loop2)}")

    # running_loop = asyncio.get_running_loop()
    # print(f"Running event loop: {running_loop}, id: {id(running_loop)}")

    thread = threading.Thread(target=thread_function, args=(f"Thread-1",))
    thread.start()
    thread.join()

# Current event loop: <_UnixSelectorEventLoop running=False closed=False debug=False>, id: 140383342024352
# Current event loop: <_UnixSelectorEventLoop running=False closed=True debug=False>, id: 140383342024352
# New event loop: <_UnixSelectorEventLoop running=False closed=False debug=False>, id: 140383333090032
# Current event loop: <_UnixSelectorEventLoop running=False closed=True debug=False>, id: 140383342024352
