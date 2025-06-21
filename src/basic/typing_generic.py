""" Python 泛型
https://typing.python.org/zh-cn/latest/reference/generics.html

泛型应用：
    泛型函数：def func[T](arg: T): ...
    泛型类：class Bag[T]: ...
    泛型类型别名：type ListOrSet[T] = list[T] | set[T]
   
TypeVar 
https://docs.python.org/zh-cn/3.13/library/typing.html#typing.TypeVar
用于构造类型变量。
def __init__(
        self, name: str, *constraints: Any, bound: Any | None = None, covariant: bool = False, contravariant: bool = False
    ) -> None: ...
TypeVar 有4种属性：
    - name: 类型变量的名称
    - constraints: 约束类型的元组，表示该类型变量可以是这些类型中的任意一个
      如果只存在类型约束不需要使用 TypeVar 定义，比如： def print_capitalized[S: str](x: S) -> S
    - bound: 该类型变量必须是指定类型的子类
    - covariant: 如果为 True，则该类型变量是协变的
    - contravariant: 如果为 True，则该类型变量是逆变的
关于类型协变、逆变和不变（TypeVar中默认是不变的）：
    - 协变（Covariant）：子类型关系保持不变，即如果 T1 是 T2 的子类型，那么 Container[T1] 也是 Container[T2] 的子类型
    - 逆变（Contravariant）：子类型关系反转，即如果 T1 是 T2 的子类型，那么 Container[T2] 是 Container[T1] 的子类型。
    - 不变（Invariant）：子类型关系不影响类型变量，即如果 T1 是 T2 的子类型，Container[T1] 和 Container[T2] 没有子类型关系
    不能同时开启 covariant 和 contravariant 属性。
TypeVar 示例
    T = TypeVar('T')  # 可以是任意类型
    S = TypeVar('S', bound=str)  # 可以是任意 str 的子类型
    A = TypeVar('A', str, bytes)  # 必须是 str 或 bytes

Generic 
泛型类隐式继承自 Generic。为了与 Python 3.11 及更低版本兼容，也允许显式地从 Generic 继承以表示泛型类
即这两种写法是等价的：
    class LoggedVar[T]:
    class LoggedVar(Generic[T]):

例子：
比如 LangGraph 中的 Command 定义：
N = TypeVar("N", bound=Hashable)
class Command(Generic[N], ToolOutputMixin):
"""

from dataclasses import dataclass
from typing import Generic, Hashable, Type, TypeVar

# -------------------------------------------------------------


def print_capitalized[S: str](x: S) -> S:
    """Print x capitalized, and return x."""
    print(x.capitalize())
    return x


print_capitalized("hello")  # 输出: Hello

# -------------------------------------------------------------


def concatenate[A: (str, bytes)](x: A, y: A) -> A:
    """Add two strings or bytes objects together."""
    return x + y

# 等同于下面写法


AT = TypeVar("AT", str, bytes)


def concatenate2[AT](x: AT, y: AT) -> AT:
    """Add two strings or bytes objects together."""
    return x + y


concatenated_str = concatenate("Hello, ", "world!")
concatenated_bytes = concatenate(b"Hello, ", b"world!")
print(concatenated_str)  # 输出: Hello, world!
print(concatenated_bytes)  # 输出: b'Hello, world!'

concatenated_str2 = concatenate2("Hello, ", "world!")
print(concatenated_str2)  # 输出: Hello, world!

# -------------------------------------------------------------

# 协变、逆变和不变


@dataclass
class AnimalToy:
    name: str

    def yell(self):
        """动物玩具发出叫声"""
        raise NotImplementedError("Subclasses should implement this method.")

    def test(self):
        print(f"Testing {self.name}...")
        self.yell()


class Dog(AnimalToy):
    def yell(self):
        print("Woof! Woof!")


class Cat(AnimalToy):
    def yell(self):
        print("Meow! Meow!")


T = TypeVar("T", bound=AnimalToy, covariant=True)
N = TypeVar("N", bound=AnimalToy, contravariant=True)

# 这两种写法是等价的，ToyProducer[T] 更推荐，更符合通用的编程规范，其他语言都是这么写的
# class ToyProducer(Generic[T]):    # 这种写法是为了兼容 Python 低版本


class ToyProducer[T]:
    # def __init__(self, toy_class: Type[T], *args, **kwargs):
    def __init__(self, toy_class: T, *args, **kwargs):
        self.toy_class = toy_class
        self.args = args
        self.kwargs = kwargs

    def get(self) -> AnimalToy:
        # Python 中的类似Java反射的写法，Python 中这种写法不是反射，对于 Python来说，类本身就是一个对象，可以直接调用
        # Dog() 其实是调用了类对象的 __call__ 方法
        # 下面这两种写法本质是一样的
        # dog = Dog()
        # 与
        # clazz = Dog
        # dog = clazz()
        # return T(*self.args, **self.kwargs)   # T 不能直接调用
        return self.toy_class(*self.args, **self.kwargs)


def use_producer(p: ToyProducer[AnimalToy]):
    animal = p.get()
    animal.yell()


# dog_producer = ToyProducer[Dog](Dog, name="Bone") # 没必要指定类型，后面的 Dog 可以反推
dog_producer = ToyProducer(Dog, name="Bone")
cat_producer = ToyProducer(Cat, name="Whiskers")

# 协变
use_producer(dog_producer)  # Dog ToyProducer 可以传递给接收 ToyProducer[AnimalToy] 的函数


class ToyTester(Generic[N]):
    def test(self, toy: N):
        print(f"Exec test {toy.name}...")
        toy.test()


def dog_test(tester: ToyTester[Dog], toy: Dog):
    tester.test(toy)


animal_toy_tester = ToyTester[AnimalToy]()
dog = dog_producer.get()

# 逆变
dog_test(animal_toy_tester, dog)  # ToyTester[AnimalToy] 可以传递给接收 ToyTester[Dog] 的函数

print(Dog)          # <class '__main__.Dog'>
print(Type[Dog])    # typing.Type[__main__.Dog]
