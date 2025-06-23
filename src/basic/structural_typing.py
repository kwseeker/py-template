"""结构化子类型（structural subtyping， 又称静态鸭子类型）
关于 名义子类型（PEP484） vs 结构子类型(PEP544)： https://docs.python.org/zh-cn/3.13/library/typing.html#nominal-vs-structural-subtyping

Structural subtyping 是一种类型系统，它通过检查对象的结构（属性和方法）来确定类型兼容性，而不是通过显式声明的类型名称。这种方式在动态语言中非常常见，如 TypeScript 和 Python 的某些类型提示。

Python 结构化子类型实现规范：https://peps.python.org/pep-0544/
Python、TS、GO 现有的结构化子类型方法: https://peps.python.org/pep-0544/#existing-approaches-to-structural-subtyping
Python 使用 Protocols 来实现结构化子类型，Protocols 是一种特殊的类型提示，它定义了一个接口，任何实现了该接口的类都可以被视为该 Protocol 的子类型。

TypedDict 
TypedDict 创建的字典类型使类型检查程序期望所有实例都有一组特定的键，其中每个键都与一致类型的值相关联。注意运行时不会对这种期望进行检查。只有在执行 mypy 等类型检查器时，才会对 TypedDict 进行类型检查。继承 TypedDict 的类的类型仍然是 dict 类型。
也即 TypedDict 仅仅是为 dict 类添加了类型检查时的类型约束，且并不是一个真正的类。
"""
from typing import Protocol, runtime_checkable
from typing import TypedDict

# ----------------------------------------------------
# 在运行时不会强制检查类型


class A:
    x: int
    y: str


class B:
    x: int
    y: str
    z: bool


class C:
    x: int
    z: bool


def foo(a: A):      # 这里的 A 相当具有迷惑性，在这个例子中其实并没有什么用
    print(a['x'])   # 这里操作的方式也是 dict 的操作方式, Python 无论类属性还是对象属性没有这种操作方式


# 这个例子自始至终都在使用 dict 对象，和 A B C 类型没有关系
b: B = {'x': 1, 'y': 'hello', 'z': True}
c: C = {'x': 2, 'z': True}    # 这样创建的 b c 本质是 <class 'dict'> 对象，不是 B C 类型对象
print(type(c))  # <class 'dict'>
foo(b)  # dict 对象能传给 A 类型参数(主要是在运行时不会强制检查类型)，且不改变类型本质，传给 a 还是 dict 对象，所以 print(a['x']) 能正常访问
foo(c)  # 同理
print("-----------------------------")

# --------------------------------------------------------------------
# 普通类还是需要通过显示类继承判断是否是子类型（名义子类型）
# 同样在运行时不会强制检查类型，所以只要后续访问方法正确，即使类型不匹配也不会报错


class M:
    def __init__(self, x: int, y: str):
        self.x = x
        self.y = y


class N:
    def __init__(self, x: int, y: str, z: bool):
        self.x = x
        self.y = y
        self.z = z


def read_x(m: M) -> int:
    print(type(m))
    return m.x


m = M(1, 'hello')
n = N(2, 'world', True)
print(isinstance(n, M))  # False
print(issubclass(N, M))  # False
print(read_x(n))         # 虽然 n 不是 M 类型的对象，但是因为默认不会检查类型，所以不会报错
print("-----------------------------")

# --------------------------------------------------------------------
# TypedDict 以类的方式创建字典类型，本质还是 dict 类型，创建的字典类型使类型检查程序期望所有实例都有一组特定的键，其中每个键都与一致类型的值相关联。注意运行时不会对这种期望进行检查。


class A2(TypedDict):
    x: int
    y: str


class B2(TypedDict):    # B 可以视为 A 的子类型
    x: int
    y: str
    z: bool


class C2(TypedDict):
    x: int
    z: bool


def foo2(a: A2):
    print(a['x'])


# b: B = B(**{'x': 1, 'y': 'hello', 'z': True})   # 普通类不支持这种写法
# b: B = B(**{'m': 1, 'n': 'hello'})
b2: B2 = B2(**{'x': 1, 'y': 'hello', 'z': True})  # 继承TypedDict的类初始化时会检查赋值的字段和类型约束是否和定义一致
b2: B2 = B2(**{'m': 1, 'n': 'hello'})             # 传定义中没有的字段不会报错
b2: B2 = B2(**{'x': 'hi', 'n': 'hello'})          # 传字段类型不一致也不会报错，因为运行时不会对这种期望进行检查，类型检查时会报错
print(b2)
print(type(b2))  # 仍然是 <class 'dict'> 对象
foo2(b2)

c2: C2 = C2(**{'x': 2, 'z': True})
foo2(c)
print("-----------------------------")

# --------------------------------------------------------------------
# Python Protocol 实现结构化子类型


@runtime_checkable  # @runtime_checkable 是一个装饰器，用于增强 typing.Protocol 的功能，使其支持 运行时类型检查（通过 isinstance() 或 issubclass()）。
class A(Protocol):
    name: str        # This is a protocol member
    value: int = 0   # This one too (with default)

    def method(self) -> str: ...    # ... 是 Python 中的占位符，表示该方法是一个抽象方法，具体实现由子类提供。


class B:  # 未继承 A，但实现了 A 的所有成员（方法和属性），所以是 A 的子类型

    def __init__(self, name: str, value: int) -> None:
        self.name = name
        self.value = value

    def method(self) -> str:
        return "hello"


class C:  # 存在未实现的 A 属性，不是 A 的子类型

    def method(self) -> str:
        return "hi"


print(isinstance(B("value", 1), A))  # True（因为 B 结构上满足 A 的协议）
print(isinstance(C(), A))  # False (因为 C 没有 name 和 value 属性)
