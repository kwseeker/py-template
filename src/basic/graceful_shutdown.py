"""优雅退出策略
两种方式: atexit 和 signal
只用 atexit 时使用键盘信号关闭程序时，日志中会抛出键盘中断和调用栈，然后执行 atexit.register 注册的函数
只用 signal 模块注册信号处理函数, 只能在信号关闭程序时才会执行资源清理
可以同时使用 atexit 和 signal 模块来实现优雅退出，这时 signal 处理方法中只需要直接退出即可
"""

import atexit
import os
import signal
import time


@atexit.register
def cleanup_resources():
    """
    通过 atexit 模块注册的函数, 在程序被未被 Python 捕获的信号杀死时并不会执行,
    在检测到 Python 内部致命错误以及调用了 os._exit() 时也不会执行.
    atexit.register(cleanup_resources)
    """
    print("Cleanup resources by atexit...")
    # Perform cleanup actions here
    time.sleep(1)
    print("Cleanup completed")

# atexit.register(cleanup_resources)


def signal_handler(signum, frame):
    print(f"Received signal {signum}, shutting down gracefully...")
    # 只需要退出即可，atexit.register(cleanup_resources) 会自动执行
    exit(0)


signal.signal(signal.SIGINT, signal_handler)
signal.signal(signal.SIGTERM, signal_handler)


def main():
    count = 0
    while count < 5:
        print("Running...")
        time.sleep(1)
        count += 1

    # 这些都不属于致命错误？
    # raise Exception("Simulating an exception to test cleanup")
    # raise SystemError("Simulating a system error to test cleanup")
    # raise MemoryError("Simulating a memory error to test cleanup")

    # 直接退出，atexit.register(cleanup_resources) 不会执行
    # os._exit(0)

    # atexit.register(cleanup_resources) 会执行
    exit(0)


if __name__ == '__main__':
    main()
