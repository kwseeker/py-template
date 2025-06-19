import asyncio
import threading
import unittest

# 下面这是两个线程本地变量 _local _running_loop


class _Local(threading.local):
    a = None


_local = _Local()


class _RunningLoop(threading.local):
    b = None


_running_loop = _RunningLoop()


class NormalClass:
    a = 0


async def read_local():
    return [_local.a, _running_loop.b]


async def set_local(arg1, arg2):
    _local.a = arg1
    _running_loop.b = arg2


async def fn():
    await asyncio.sleep(1)


class TestEventLoop(unittest.TestCase):
    def test_1(self):
        """测试同时使用 asyncio.get_event_loop() asyncio.run()"""
        # 这两行中获取的 loop 并不一样
        # 这行逻辑是(Python 3.12.10)：如果是主线程优先从线程本地 (_Local) 取，没有使用策略工厂创建，然后保存到主线程本地，如果不是主线程，直接使用策略工厂创建且不会保存到线程本地
        # Python3.12 的实现则是直接使用策略工厂创建，然后存到线程本地
        loop = asyncio.get_event_loop()
        print(f"loop id: {id(loop)}")
        loop.close()
        # 这行逻辑是：如果是主线程且有运行的 event_loop 会报错 (_RunningLoop)，asyncio.run 必须是使用自己新建的 event_loop
        asyncio.run(fn())

    def test_2(self):
        ret = asyncio.run(read_local())
        print(ret)
        asyncio.run(set_local(1, 2))
        ret = asyncio.run(read_local())
        print(ret)

    def test_3(self):
        nc1 = NormalClass()
        nc2 = NormalClass()
        # 这里其实不是访问的类属性a 而是实例属性a, 类属性a只不过是提供实例属性a未赋值时的默认值
        print(nc1.a)
        nc1.a = 3
        nc2.a = 4
        nc2.b = 5
        print(nc1.a)
        print(nc2.a)
        print(nc2.b)
        print(NormalClass.a)


if __name__ == "__main__":
    unittest.main()
