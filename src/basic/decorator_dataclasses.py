""" dataclasses
https://docs.python.org/3/library/dataclasses.html

该模块提供了一个装饰器和函数，用于自动向用户定义的类中添加生成的特殊方法，如 __init__() 和 __repr__() 。

可以通过下面参数控制生成哪些特殊方法：
@dataclass 等同于
@dataclass(init=True, repr=True, eq=True, order=False, unsafe_hash=False, frozen=False,
           match_args=True, kw_only=False, slots=False, weakref_slot=False)
"""

from dataclasses import dataclass

# kw_only=True: 所有字段必须通过关键字赋值, 即只能 Point(x=1.0, y=2.0) 这么传参，不能 Point(1.0, 2.0) 这么传参
# slots=True: 使用更省内存的方式存储属性
# frozen=True: 类实例不可变（像元组一样）
_DC_KWARGS = {"kw_only": True, "slots": True, "frozen": True}


@dataclass(**_DC_KWARGS)
class Point:
    x: float = 0.0
    y: float = 0.0
    # color: str = "black"


# __init__()
# p = Point(1.0, 2.0)  # 报错
p = Point(x=1.0, y=2.0)

# __repr__()
print(p)

# __eq__()
p2 = Point(x=1.0, y=2.0)
print(p == p2)  # True

# __match_args__ 属性，返回一个元组，定义类在模式匹配中解包时的字段顺序
# 不包含仅接受关键字赋值的参数，开启 kw_only=True 后，__match_args__ 为空, 且后面模式匹配时只能匹配 Point()
print(p.__match_args__)


def desc_point(point):
    match point:    # 模式匹配
        # case Point(x, y):
        case Point():
            # print(f"Point with x: {x} and y: {y}")
            print(f"Point with no none keyword-only args")
        case _:
            print("Not a Point instance")


desc_point(p)
