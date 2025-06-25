"""Annotated
为一个类型添加与其使用上下文相关的元信息；
Annotated 是 Python 提供的一种机制，用于在不改变类型行为的前提下为其附加额外信息，广泛应用于验证、文档生成、AI Agent 状态管理等领域。它支持嵌套展平、类型别名定义等功能，但不能与展开的 TypeVarTuple 结合使用。
示例：
    Annotated[int, runtime_check.Unsigned] 
    表示向假设的 runtime_check 模块表明这个类型是一个无符号整数。
    其他任何使用该类型的模块都可以忽略这些元信息，并将其视为普通的 int 类型。
    
    Annotated 的第一个参数必须是一个合法的类型。
    如果调用 Annotated 时传入的参数少于两个(包括第一个类型参数)，将产生错误。
"""
from typing import Annotated, get_type_hints, Union
from functools import wraps

# 自定义标记类作为规则描述


class Positive:
    def validate(self, value):
        if value <= 0:
            raise ValueError("值必须大于 0")
        return value


class NonEmpty:
    def validate(self, value):
        if not value:
            raise ValueError("值不能为空")
        return value

# 包装器：用于自动应用 Annotated 中的规则


def apply_annotations(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        # get_type_hints() 是 Python 标准库中 typing 模块提供的一个函数，用于获取函数、类或模块的类型提示信息。
        # 它在类型检查、文档生成、框架设计等领域有广泛应用
        # 函数签名：
        #   typing.get_type_hints(obj, globalns=None, localns=None, *, include_extras=False)
        #   obj: 要提取类型注解的对象：函数、类或模块
        #   globalns=None, localns=None: 可选命名空间，用于解析字符串形式的类型注解（如 'MyClass'）
        #   include_extras: 是否包含额外信息（如 Annotated 中的元数据），默认为 False
        #       比如：
        #       def demo(x: Annotated[int, "positive", "range(1, 100)"]): ...
        #       print(get_type_hints(demo))
        #           默认输出: {'x': int, 'return': None}
        #       print(get_type_hints(demo, include_extras=True))
        #           输出: {'x': Annotated[int, 'positive', 'range(1, 100)'], 'return': None}
        hints = get_type_hints(func, include_extras=True)

        new_kwargs = {}
        for name, hint in hints.items():
            if name in kwargs:
                value = kwargs[name]
                # 检查是否为 Annotated 类型
                if hasattr(hint, '__metadata__'):
                    for metadata in hint.__metadata__:
                        if hasattr(metadata, 'validate'):
                            value = metadata.validate(value)
                new_kwargs[name] = value
        return func(**new_kwargs)
    return wrapper


# 使用 Annotated 添加规则注解
@apply_annotations
def greet(name: Annotated[str, NonEmpty()], age: Annotated[int, Positive()]):
    print(f"Hello {name}, you are {age} years old.")


print(greet.__annotations__)

# 正确调用
greet(name="Alice", age=30)  # 成功

# 错误调用（会抛异常）
try:
    greet(name="", age=25)
except ValueError as e:
    print("错误1:", e)

try:
    greet(name="Bob", age=-5)
except ValueError as e:
    print("错误2:", e)
