"""类型窄化
    TypeIs 和 TypeGuard 其实是函数，返回 True 或 False
    都用于判断变量类型能否窄化到目标类型。
    TypeGurad 更灵活（限制更少），比如如下场景：
    1. 将类型缩小到不兼容类型，如从 list[object] 到 list[int] 。 TypeIs 仅允许在兼容类型之间进行缩小
        但是这也可能带来不安全问题。
    2. 不对所有缩小类型的输入值返回 True, 比如下面代码，使用 TypeIs 就是错误的写法，但是使用 TypeGurad 是正确的
        # 反面案例：
        #   TypeIs 初衷是判断变量是否可以窄化到某个类型，但是这里仅仅正整数会返回True
        #   0 和 负整数明明也可以窄化到 int, 却返回 False
        def is_positive_int(x: object) -> TypeIs[int]:      
            return isinstance(x, int) and x > 0
        # 正面案例：
        def is_positive_int(x: object) -> TypeGurad[int]:
            return isinstance(x, int) and x > 0
"""

from typing import (
    TypeGuard,
    Literal,
    TypedDict,
    Any,
    Union,
    List,
    Optional,
    Sequence,
    final,
)
from typing_extensions import TypeIs    # 3.13 之后 TypeIs 才移动到 typing 模块
import asyncio
from dataclasses import dataclass
import unittest

# --------------------------
# 1. 基础类型收窄 (Type Narrowing)
# --------------------------


# def maybe_greet(name: Optional[str]) -> None:
def maybe_greet(name: str | None) -> None:
    """通过 `if name is not None` 收窄类型"""
    if name is not None:
        print(f"Hello, {name}")  # name 被收窄为 str
    else:
        print("Hello, Guest")


# def process_value(value: Union[int, str]) -> None:
def process_value(value: int | str) -> None:
    """通过 `isinstance` 收窄类型"""
    if isinstance(value, int):
        print(f"Value is an integer: {value + 1}")  # value 被收窄为 int
    else:
        print(f"Value is a string: {value.upper()}")  # value 被收窄为 str


# --------------------------
# 2. 用户自定义类型收窄 (TypeIs)
# --------------------------
Direction = Literal["N", "E", "S", "W"]


def is_direction(x: str) -> TypeIs[Direction]:
    """自定义 TypeIs 函数，检查是否为方向"""
    return x in {"N", "E", "S", "W"}


def check_direction(x: str) -> None:
    """使用 TypeIs 函数收窄类型"""
    if is_direction(x):
        print(f"{x} is a valid direction")  # x 被收窄为 Direction
    else:
        print(f"{x} is not a direction")  # x 保持为 str


class Point(TypedDict):
    """用于测试复杂类型的 TypeIs"""
    x: int
    y: int


def is_point(obj: object) -> TypeIs[Point]:
    """检查对象是否符合 Point 类型"""
    return (
        isinstance(obj, dict)
        and all(isinstance(key, str) for key in obj)
        and isinstance(obj.get("x"), int)
        and isinstance(obj.get("y"), int)
    )


def use_point(obj: object) -> None:
    """测试 TypedDict 的 TypeIs 收窄"""
    if is_point(obj):
        print(f"Point coordinates: ({obj['x']}, {obj['y']})")  # obj 被收窄为 Point
    else:
        print("Not a valid point")

# --------------------------
# 3. TypeGuard 的用法
# --------------------------


def is_int_list(x: List[Any]) -> TypeGuard[List[int]]:
    """检查列表是否全为整数 (TypeGuard)"""
    return all(isinstance(i, int) for i in x)


def process_list(x: List[Any]) -> None:
    """使用 TypeGuard 收窄列表类型"""
    if is_int_list(x):
        print(f"Sum of integers: {sum(x)}")  # x 被收窄为 List[int]
    else:
        print("List contains non-integers")

# --------------------------
# 4. TypeIs 和 TypeGuard 的区别
# --------------------------


@final
class Base:
    pass


@final
class Child(Base):
    pass


@final
class Unrelated:
    pass


def is_base_typeguard(x: object) -> TypeGuard[Base]:
    """TypeGuard 示例"""
    return isinstance(x, Base)


def is_base_typeis(x: object) -> TypeIs[Base]:
    """TypeIs 示例"""
    return isinstance(x, Base)


# def demonstrate_difference(x: Union[Child, Unrelated]) -> None:
def demonstrate_difference(x: Child | Unrelated) -> None:
    """展示 TypeIs 和 TypeGuard 的区别"""
    if is_base_typeguard(x):
        # TypeGuard: 收窄到 Base (忽略原始类型)
        print(f"TypeGuard narrowed to Base: {type(x)}")
    else:
        print("TypeGuard did not narrow")

    if is_base_typeis(x):
        # TypeIs: 收窄到 Child (保留原始类型的交集)
        print("TypeIs narrowed to Child")
    else:
        print("TypeIs narrowed to Unrelated")

# --------------------------
# 5. 不安全场景测试
# --------------------------


def unsafe_typeguard_example() -> None:
    """展示 TypeGuard 的潜在不安全行为"""
    def is_int_list_bad(x: List[Any]) -> TypeGuard[List[int]]:
        return len(x) > 0  # 错误实现：未实际检查类型

    data: List[str] = ["a", "b", "c"]
    if is_int_list_bad(data):
        # 错误地收窄为 List[int]，但运行时会导致 TypeError
        print(sum(data))  # 运行时错误

# --------------------------
# 6. 异步环境下的类型收窄问题
# --------------------------


async def async_narrowing_issue() -> None:
    """展示异步代码中类型收窄的失效问题"""
    shared_list: List[Optional[int]] = [1, 2, 3]

    def is_all_int(x: Sequence[Optional[int]]) -> TypeIs[Sequence[int]]:
        return all(isinstance(i, int) for i in x)

    async def task1() -> None:
        if is_all_int(shared_list):
            await asyncio.sleep(1)
            print(f"Sum: {sum(shared_list)}")  # 可能运行时失败

    async def task2() -> None:
        await asyncio.sleep(0.5)
        shared_list.append(None)  # 在其他任务中修改数据

    await asyncio.gather(task1(), task2())

# --------------------------
# 单元测试
# --------------------------


class TestTypeNarrowing(unittest.TestCase):
    def test_typeis_direction(self):
        self.assertTrue(is_direction("N"))  # 应返回 True
        self.assertFalse(is_direction("X"))  # 应返回 False

    def test_typeguard_list(self):
        self.assertTrue(is_int_list([1, 2, 3]))  # 应返回 True
        self.assertFalse(is_int_list(["a", "b"]))  # 应返回 False

    def test_unsafe_typeguard(self):
        with self.assertRaises(TypeError):
            unsafe_typeguard_example()  # 预期运行时错误


if __name__ == "__main__":
    # 运行示例
    maybe_greet("Alice")  # 输出: Hello, Alice
    maybe_greet(None)     # 输出: Hello, Guest

    check_direction("N")  # 输出: N is a valid direction
    check_direction("X")  # 输出: X is not a direction

    use_point({"x": 1, "y": 2})  # 输出: Point coordinates: (1, 2)
    use_point({"x": "a"})         # 输出: Not a valid point

    process_list([1, 2, 3])      # 输出: Sum of integers: 6
    process_list(["a", "b"])     # 输出: List contains non-integers

    demonstrate_difference(Child())    # 输出差异对比
    demonstrate_difference(Unrelated())

    # 运行异步测试（注意：此示例会抛出运行时错误）
    # asyncio.run(async_narrowing_issue())

    # 运行单元测试
    unittest.main()
