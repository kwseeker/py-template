""" 
    1 with 语句: 
        功能: 
            https://peps.python.org/pep-0343/
            with 语句提供了一种上下文管理协议的方式来管理资源, 比如文件操作、网络连接等。它确保在进入和退出代码块时执行必要的设置(__enter__)和清理(__exit__)工作。
            类似Java try(...) { } 语句,  可以自动做资源清理工作
            不过 with 修饰的对象必须实现 __enter__ 和 __exit__ 方法
        比如：
            with VAR = EXPR:
                BLOCK
        等同于：
            VAR = EXPR
            VAR.__enter__()
            try:
                BLOCK
            finally:
                VAR.__exit__()
    2 with ... as ... 语句:
        比如：
            with EXPR as VAR:   # 注意这里不是将 EXPR 表达式的结果赋值给VAR, 而是将表达式结果传参给__enter__然后将返回值赋值给VAR
                BLOCK
        等同于：
            mgr = (EXPR)
            exit = type(mgr).__exit__  # Not calling it yet
            value = type(mgr).__enter__(mgr)
            exc = True
            try:
                try:
                    VAR = value  # Only if "as VAR" is present
                    BLOCK
                except:
                    # The exceptional case is handled here
                    exc = False
                    if not exit(mgr, *sys.exc_info()):
                        raise
                    # The exception is swallowed if exit() returns true
            finally:
                # The normal and non-local-goto cases are handled here
                if exc:
                    exit(mgr, None, None, None)

    3 async with ... as ... 语句
        with ... as ... 的异步版本，另外异步上下文管理器必须定义 __aenter__() 和 __aexit__() 协程方法。
        会等待with后面的语句执行完成
        详细参考 aiomysql 中的实现
        
    4 上下文管理器协议
        是指在Python中一个对象如果要与with语句一起使用必须实现的特殊方法集。
        具体来说，这些方法包括：
        __enter__(): 在进入with代码块时被调用。这个方法通常用于设置一些资源, 比如打开文件或获取锁, 并返回一个对象, 该对象在with块中可以被使用。
        __exit__(exc_type, exc_value, traceback): 在退出with代码块时被调用, 无论代码块是否抛出异常。这个方法接收三个参数: 
            exc_type: 如果with块中发生异常, 这是异常类型；如果没有异常, 则为None。
            exc_value: 如果发生异常, 这是异常实例；如果没有异常, 则为None。
            traceback: 如果发生异常, 这是跟踪回溯对象；如果没有异常, 则为None。
    """


import asyncio


class SyncResource:
    def __enter__(self):
        print("开始同步资源")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("结束同步资源")


class AsyncResource:
    async def __aenter__(self):
        print("开始异步资源")
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        print("结束异步资源")


async def main():
    async with AsyncResource() as resource:
        print("正在使用异步资源")

if __name__ == "__main__":
    with SyncResource() as resource:
        print("正在使用同步资源")

    asyncio.run(main())
