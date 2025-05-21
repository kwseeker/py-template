"""
get_event_loop() 用于获取线程事件循环对象，对于主线程来说如果事件循环不存在会主动创建并存储到主线程线程本地
非主线程调用 get_event_loop() 会抛出错误
不过一个线程却可以创建多个事件循环，只不过只有主线程通过 get_event_loop() 获取的事件循环对象才会存储到主线程的线程本地
"""

import asyncio
import threading


async def hello():
    print("Hello, world!")
    await asyncio.sleep(1)


def thread_function(name):
    print(f"线程 {name} 开始")
    loop = asyncio.new_event_loop()
    # loop = asyncio.get_event_loop()
    loop.run_until_complete(hello())
    loop2 = asyncio.new_event_loop()
    print(f"New event loop: {loop}, id: {id(loop)}")
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
    loop2 = asyncio.get_event_loop()
    print(f"Current event loop: {loop2}, id: {id(loop2)}")

    thread = threading.Thread(target=thread_function, args=(f"Thread-1",))
    thread.start()
    thread.join()

# Current event loop: <_UnixSelectorEventLoop running=False closed=False debug=False>, id: 140383342024352
# Current event loop: <_UnixSelectorEventLoop running=False closed=True debug=False>, id: 140383342024352
# New event loop: <_UnixSelectorEventLoop running=False closed=False debug=False>, id: 140383333090032
# Current event loop: <_UnixSelectorEventLoop running=False closed=True debug=False>, id: 140383342024352
