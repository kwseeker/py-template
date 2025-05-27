"""Python 生成器
    在 Python 中，使用了 yield 的函数被称为生成器（generator）。
    yield 是一个关键字，用于定义生成器函数，生成器函数可以在迭代过程中逐步产生值，而不是一次性返回所有结果。
    生成器是一个返回迭代器的函数，只能用于迭代操作，更简单点理解生成器就是一个迭代器。

    Python 迭代器：
    1. iter() next()
    2. for 遍历迭代器
    3. 迭代器对象 __iter__() __iter__()
    4. 使用 StopIteration 异常可以标识迭代结束
"""


import sys


def countdown(n):
    """一个生成器函数"""
    while n > 0:
        yield n
        n -= 1


generator = countdown(5)

# 通过迭代生成器获取值
print(next(generator))  # 输出: 5
print(next(generator))  # 输出: 4
print(next(generator))  # 输出: 3

# 使用 for 循环迭代生成器获取值
for value in generator:
    print(value)  # 输出: 2 1


def fibonacci(n):
    """生成器实现斐波那契"""
    a = 0
    b = 1
    counter = 0
    while True:
        if (counter > n):
            return
        yield a
        a, b = b, a + b
        counter += 1


f = fibonacci(10)  # f 是一个迭代器，由生成器返回生成

while True:
    try:
        print(next(f), end=" ")
    except StopIteration:
        sys.exit()
