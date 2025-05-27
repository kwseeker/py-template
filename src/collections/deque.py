""" collections 标准库 deque 对象
    https://docs.python.org/zh-cn/3.13/library/collections.html#collections.deque
        
    1. 双端队列
    2. 支持线程安全
    3. 默认从后侧插入、推出元素： append() pop(), 如果从左侧操作使用 appendleft() popleft()
    4. maxlen 不指定或为 None, 则长度任意，否则当容量满后插入元素会从另一端弹出元素
    5. 支持 for 循环遍历， 继承的基类有实现迭代器方法 __iter__()
"""

import collections


def print_elements(q: collections.deque):
    for e in q:
        print(f"{e} ", end='')
    print()


q = collections.deque("abc")
# 从右侧插入
q.append("d")
print_elements(q)

# 从右侧弹出
q.pop()

q.extend(["e", "f", "g"])
print_elements(q)

q.rotate(3)
print_elements(q)

print(f"maxlen: {q.maxlen}")
