"""Python 生成器
    Python 迭代器：
    1. iter() next()
    2. for 遍历迭代器
    3. 迭代器对象 __iter__() __iter__()
    4. 使用 StopIteration 异常可以标识迭代结束

    在 Python 中，使用了 yield 的函数被称为生成器（generator）。
    yield 是一个关键字，用于定义生成器函数，生成器函数可以在迭代过程中逐步产生值，而不是一次性返回所有结果。
    生成器是一个返回迭代器的函数，只能用于迭代操作，更简单点理解生成器就是一个迭代器。
    
    生成器的本质：
        生成器函数也是一个语法糖，本质是迭代器对象
        比如：
            一个生成器函数：
                def firstn(n):
                    num = 0
                    while num < n:
                        yield num
                        num += 1
            本质是：
                class first_n(object):

                    def __init__(self, n):
                        self.n = n
                        self.num = 0
              
                    def __iter__(self):
                        return self

                    def __next__(self):
                        return self.next()

                    def next(self):
                        if self.num < self.n:
                            cur, self.num = self.num, self.num+1
                            return cur
                        raise StopIteration()

        https://wiki.python.org/moin/Generators
    
    生成器-迭代器的方法:
        https://docs.python.org/zh-cn/3.13/reference/expressions.html#generator-iterator-methods
        
        generator.__next__() 开始一个生成器函数的执行或是从上次执行 yield 表达式的位置恢复执行。此方法通常是隐式地调用，例如通过 for 循环或是内置的 next() 函数。
        generator.send(value)
        generator.throw(value)
        generator.throw(type[, value[, traceback]])  在生成器暂停的位置引发一个异常，并返回该生成器函数所产生的下一个值。 如果生成器没有产生下一个值就退出，则将引发 StopIteration 异常。 如果生成器函数没有捕获传入的异常，或是引发了另一个异常，则该异常会被传播给调用方
        generator.close() 在生成器函数暂停的位置引发 GeneratorExit。 如果生成器函数捕获该异常并返回一个值，这个值将从 close() 返回。 如果生成器函数已经关闭，或者引发了 GeneratorExit (由于未捕获异常)，close() 将返回 None。
        
        协程也具有 send throw close 方法，它们类似于生成器的对应方法。 但是，与生成器不同，协程并不直接支持迭代。

    异步生成器-迭代器方法：
        https://docs.python.org/zh-cn/3.13/reference/expressions.html#asynchronous-generator-iterator-methodshttps://docs.python.org/zh-cn/3.13/reference/expressions.html#asynchronous-generator-iterator-methods
    
    yield from 语法：    
        https://docs.python.org/3/whatsnew/3.3.html#pep-380-syntax-for-delegating-to-a-subgenerator
"""


import sys

# --------------------------------------------


def countdown(n):
    """一个生成器函数"""
    while n > 0:
        yield n
        yield -n        # 可以包含多个yield
        n -= 1


generator = countdown(5)    # 5 次循环 × 每次循环 2 个yield = 10 次迭代

# 通过迭代生成器获取值
print(next(generator))  # 输出: 5
print(next(generator))  # 输出: -5
print(next(generator))  # 输出: 4

# 使用 for 循环迭代生成器获取值
print("get value by for: ")
for value in generator:
    print(value)  # 输出: -4 3 -3 2 -2 1 -1

# --------------------------------------------


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
    except StopIteration:       # 没有值还迭代地话会抛StopIteration异常，所以需要捕捉异常，在迭代完后跳出循环
        # sys.exit()
        break
print()

# --------------------------------------------


def gen_none():
    yield None


generator = gen_none()

print(next(generator))  # None
# print(next(generator))  # StopIteration, 没有值还迭代地话会抛异常


def echo(value=None):
    print("Execution starts when 'next()' is called for the first time.")
    try:
        while True:
            try:
                # 这里是双向通信生成器的写法，意思是 yield 返回 value, 然后将 send 传过来的值保存到 value
                value = (yield value)
                print(f"while: {value}")
            except Exception as e:
                value = e
    finally:
        print("Don't forget to clean up when 'close()' is called.")


generator = echo(1)
# None, 这行 next(generator) 相当于 generator.send(None), 即 value = (yield value) 相当于 先 yield 1 再 value = None
print(next(generator))
print(next(generator))  # None
generator.send("A")
print(next(generator))  # A
generator.close()

# --------------------------------------------


def sub_gen():
    for i in range(5):
        yield i
    return 100


def gen():
    """ 
    yield from 相当于下面代码的简写
    g = sub_gen()
    while True:
        try:
            temp = next(g)
            yield temp
        except StopIteration as e:
            print(f"sub_gen return: {e.value}")
            return
    """
    sg = sub_gen()
    res = yield from sg
    print(f"sub_gen return: {res}")
    return res


for i in gen():         # for 只能读取 yield 返回的数据，无法读取 gen() 中 retrun 的数据
    print(f"{i} ", end="")
# res = gen()           # gen() 返回一个生成器
# print(f"res: {res}")

# --------------------------------------------


def accumulate():
    tally = 0
    while 1:
        # 生成器的接收发送模式：
        # 当外部调用 send(value) 时，value 会赋值给 next
        # 首次必须用 next() 或 send(None) 启动生成器（执行到第一个 yield 暂停）, 执行到第一个 yield 暂停可以理解为执行了一次数据读取迭代
        # yield 后面为空表示只接收数据不产出数据，注意连 None 都不产出
        next = yield
        print(f"received: {next}")
        # 如果外部 send None 则退出生成器
        if next is None:
            return tally
        tally += next


def gather_tallies(tallies):    # 使用 yield from 则也是一个生成器
    while 1:
        # 因为 accumulate() 不产出值，gather_tallies() 也不会产出值
        # tally 接收 accumulate() 退出的值，不是接收外部 send 发送的值
        tally = yield from accumulate()
        print(tally)
        tallies.append(tally)


tallies = []
acc = gather_tallies(tallies)

next(acc)  # Ensure the accumulator is ready to accept values
for i in range(4):
    acc.send(i)

acc.send(None)  # accumulate() 中定义发送 None 会退出生成器
for i in range(5):
    acc.send(i)

acc.send(None)  # Finish the second tally

print(tallies)  # 10， 0+1+2+3+4


print(sys.path)
print(sys.modules)
