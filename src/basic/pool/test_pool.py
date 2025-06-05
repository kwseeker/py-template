import os
import asyncio
import time
from src.basic.pool.pool import Pool

pypath = os.environ.get("PYTHONPATH")
print(f"pypath: {pypath}")

loop = asyncio.get_event_loop()
print(f"loop id: {id(loop)}")
pool = Pool(2, 4, 300, loop=loop)


async def async_task():
    async with pool.acquire() as conn:
        print(f"use conn object: {conn.info()}, begin: {time.time()}")
        # 模拟业务执行
        await asyncio.sleep(1)
        # time.sleep(1)
        print(f"use conn object: {conn.info()} done, end: {time.time()}")


async def test_pool():
    tasks = [loop.create_task(async_task()) for _ in range(5)]
    await asyncio.gather(*tasks)

if __name__ == "__main__":
    # asyncio.run(test_pool())
    loop.run_until_complete(test_pool())
