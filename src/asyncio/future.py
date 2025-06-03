""" asyncio future
    https://docs.python.org/zh-cn/3.13/library/asyncio-future.html
"""

import asyncio
from asyncio import Future


async def read_future(fut):
    result = await fut
    print("Future result:", result)


async def write_future(fut: Future):
    fut.set_result("done")


async def main():
    loop = asyncio.get_event_loop()
    fut = loop.create_future()
    print(f"loop type: {type(loop)}, fut type: {type(fut)}")

    task = loop.create_task(read_future(fut))
    task2 = loop.create_task(write_future(fut))
    print(f"task type: {type(task)}")

    # 1
    # await asyncio.gather(task, task2)

    # 2
    await task
    await task2

    # 3
    # tasks = [task, task2]
    # await asyncio.wait(tasks)

if __name__ == "__main__":
    asyncio.run(main())
