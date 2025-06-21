"""Literal 是从 Python 3.8 开始，在标准库 typing 中引入的一个类型注解工具（在 Python 3.9+ 中更稳定），它允许你明确告诉开发者或类型检查器（如 mypy、Pyright）：某个变量只能是几个特定的值。
"""

from typing import Literal


def move(direction: Literal["up", "down", "left", "right"]):
    print(f"Moving {direction}")


move("up")
move("left")
move("north")   # 执行时不会报错，类型检查器执行时会报警
