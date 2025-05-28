import itertools

# for i in itertools.count(1):
#     if i > 10:
#         break
#     print(i)


def is_used(street: str, number: int) -> bool:
    # 假设这是一个外部查询函数
    return (street == "Main St" and number in [1, 2, 3, 10, 11, 12])


def lowest_unused(street: str) -> int:
    # itertools.count(1) 是一个迭代器工具，返回 1,2,3...
    for i in itertools.count(1):
        if not is_used(street, i):
            return i
    # 由于上面 for i in itertools.count(1) 要么无线迭代要么退出，这里根本不会执行
    # 但是低版本的类型检查器无法直到这一点，如果没有下面一句，类型检查器会抱怨函数缺少返回语句
    # 不过 3.12 版本测试并没有这个问题，下面这行删掉也没有问题
    assert False, "This line is unreachable"


# 调用示例
print(lowest_unused("Main St"))  # 可能输出 1, 2, ..., 直到找到第一个未使用的号码
