"""使用 assert_never() 进行穷举检查（Exhaustiveness Checking）
原理是 assert_never() 中会抛错误 AssertionError, 当 match 或 if 语句没有处理所有情况时会走到 assert_never() 这个本不应该执行的函数中，
然后通过抛错误警告有一种情况没有被处理。
"""

from enum import Enum
from typing import assert_never  # Python 3.11+ 支持


class Op(Enum):
    ADD = "add"
    SUBTRACT = "subtract"
    MULTIPLY = "multiply"


def calculate(left: int, op: Op, right: int) -> int:
    match op:
        case Op.ADD:
            return left + right
        case Op.SUBTRACT:
            return left - right
        case _:
            assert_never(op)


print(calculate(5, Op.ADD, 3))      # 输出 8
print(calculate(5, Op.SUBTRACT, 3))  # 输出 2
print(calculate(5, Op.MULTIPLY, 3))  # 由于没有处理这种情况，会报错


# def process(value: Union[int, str]) -> None:
def process(value: int | str | float) -> None:      # 新版本推荐这么写
    match value:
        case int():
            print("Processing integer:", value)
        case str():
            print("Processing string:", value)
        case _:
            assert_never(value)


process(1)
process("hi")
process(1.2)     # 由于没有处理这种情况，会报错
