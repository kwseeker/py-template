import os
import asyncio
import time
from src.basic.pool.pool import Pool

pypath = os.environ.get("PYTHONPATH")
print(f"pypath: {pypath}")

loop = asyncio.get_event_loop()
pool = Pool(2, 4, 300, loop=loop)


async def async_task():
    async with pool.acquire() as conn:
        print(f"use conn object: {conn.info()}, begin: {time.time()}")
        # 模拟业务执行
        await asyncio.sleep(1)
        # time.sleep(1)
        print(f"use conn object: {conn.info()} done, end: {time.time()}")


async def test_pool():
    await asyncio.gather(async_task(), async_task(), async_task(), async_task(),
                         async_task())

if __name__ == "__main__":
    asyncio.run(test_pool())
