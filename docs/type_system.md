# 类型系统

类型系统：https://typing.python.org/en/latest/index.html

## 1 类型系统

官方没有说明类型系统的定义和作用，直接放了一堆文档。

以下是 AI 给的定义：

“Python 的类型系统（Type System）在语言的发展中经历了从 **动态类型** 到 **渐进式类型**（通过类型注解支持**静态类型检查**）的演变。它的核心作用是为代码提供更强的 **可读性、可维护性和可靠性**，同时保持 Python 的灵活性。”

即 Python 类型系统**支持了 Python 静态类型**。

**渐进式类型是现代语言发展的趋势**（比如 TS 的流行、Python 的静态类型支持）。

### 1.1 静态类型  vs 动态类型

静态类型代表语言：Java、C++、Go、Rust、TypeScript。

动态类型代表语言：Python、JavaScript、Ruby、PHP（Python 通过其类型系统支持静态类型检查）。

| **特性**     | **静态类型**             | **动态类型**         |
| :--------- | :------------------- | :--------------- |
| **类型检查时机** | 编译时/静态检查             | 运行时              |
| **错误发现时间** | 早期（开发阶段）             | 晚期（运行时可能崩溃）      |
| **代码灵活性**  | 低（类型固定）              | 高（类型可动态改变）       |
| **开发速度**   | 较慢（需写类型）             | 较快（无需类型）         |
| **维护性**    | 高（类型即文档）             | 低（需依赖注释或测试）      |
| **性能**     | 高（编译器优化）             | 较低（运行时类型检查）      |
| **适合场景**   | **大型项目、长期维护、高可靠性需求** | **快速原型、脚本、小型项目** |

### 1.2 类型系统包含的内容

+ **类型化的python库**

  提供了类型注解、内联类型实践等指导说明。

+ **编写和维护存根文件**

+ **使用新类型功能对代码进行现代化改造**

  即使用新类型功能替换旧的实现方式。

+ **不可达代码和穷举检查**

  不可达代码指不会执行到的代码，但是有时需要加上不可达代码否则可能报错；

  穷举检查指在`match-case` 或 `if-elif-else` 结构中确保所有情况都被处理（所有情况都有对应的处理代码）。

+ **类型窄化**

  指变量、实例属性、序列成员等可能是多种类型，通过条件检查等区分实际类型的技术称为类型窄化。

  类型系统还包含两种创建用户自定义类型窄化函数的方式： `typing.TypeIs` 和 `typing.TypeGuard` 。

+ **使用类型系统编程参考**（可以理解为静态类型编程）
  
  + **泛型**
  + **预定义协议类**
  + **子类型协议与继承**
  + **一些常用的协议类**
  + **类型的最佳实现**

## 2 **类型化的python库**

提供类型注解的4种方式：

+ **内联类型注解**（推荐）

  即直接在 .py 文件中使用类型注解。比如：

  ```python
  def greet(user: str) -> None:	# 这里 ：str 就是内联类型注解
  	...
  ```

+ **包中包含的类型存根文件**

  即使用**存根文件**（Stub Files，**.pyi**）为模块或库提供静态类型信息（尤其是那些本身没有类型注解的代码）。

  有点像 C 语言的 .h 文件。

  比如为模块函数添加类型信息：

  ```python
  # calculator.py（无类型注解）
  def add(a, b):
      return a + b
  
  # calculator.pyi (在存根文件.pyi中为无类型注解的函数添加类型信息)
  def add(a: int, b: int) -> int: ... 
  ```

+ 一个独立的类型存根配套包

  在单独的包目录（后缀：-stubs）下存放类型存根。

+ typeshed 仓库中的类型存根

## 3 编写和维护存根文件

参考 [type_system_stub_files.md](./type_system_stub_files.md)

## 4 使用新类型功能对代码进行现代化改造

即使用新类型功能替换旧的实现方式。

pyupgrade、ruff 和/或 com2ann 等工具可以自动为您执行其中的一些重构。

官方文档提供了几个例子：

```python
x = 3  # type: int
def f(x, y):  # type: (int, int) -> int
    return x + y
# 替换为
x: int = 3
def f(x: int, y: int) -> int:
    return x + y

from typing import Text
def f(x: Text) -> Text: 
    ...
# 替换为 
def f(x: str) -> str: 
    ...
    
from typing import TypedDict
FlyingSaucer = TypedDict("FlyingSaucer", {"x": int, "y": str})
FlyingSaucer = TypedDict("FlyingSaucer", x=int, y=str)
# 替换为 
class FlyingSaucer(TypedDict):
    x: int
    y: str
        
from typing import Dict, List	# typing 模块为接受类型参数的内置类型提供了别名。自 Python 3.9 以来，这些别名不再必要，并且可以用内置类型来替代
def f(x: List[int]) -> Dict[str, int]: 
    ...
# 替换为
def f(x: list[int]) -> dict[str, int]: 
    ...

from typing import Optional, Union
def f(x: Optional[int]) -> Union[int, str]: 
    ...
# 替换为 
def f(x: int | None) -> int | str: 
    ...
    
# 类型别名定义
IntList = list[int]
# 替换为 （ >=3.12 ）
type IntList = list[int]

# 用户自定义泛型
# 3.12 之前泛型类必须从 typing.Generic （或另一个泛型类）派生，并使用 typing.TypeVar 定义类型变量
from typing import Generic, TypeVar
T = TypeVar("T")
class Brian(Generic[T]): ...
class Reg(int, Generic[T]): ...
# 替换为 （ >=3.12 ）
class Brian[T]: ...
class Reg[T](int): ...
```

## 5 不可达代码和穷举检查

**使用 assert_never() 进行穷举检查（Exhaustiveness Checking）**：

原理是 assert_never() 会抛错误 AssertionError, 当 match 或 if 语句没有处理所有情况时会走到 assert_never() 这个本不应该执行的函数中，然后通过抛错误警告有一种情况没有被处理。

```python
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
```

**标记不可能执行到的代码为 unreachable**：

测试 Python 3.12 并没有这个问题。

```python
import itertools


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
```

**mypy --warn-unreachable 检测不可达的代码**：

```python
def foo(x: int) -> str:
    if x > 0:
        return "positive"
    elif x < 0:
        return "negative"
    else:
        return "zero"
    # 下面这行是不可达的，因为上面已经 return 了
    print("This will never be printed")


print(foo(2))

# mypy --warn-unreachable your_file.py # 检测不可到的代码
```

## 6 类型窄化

指变量、实例属性、序列成员等可能是多种类型，通过条件检查等区分实际类型的技术称为类型窄化。

```python
def maybe_greet(name: str | None) -> None:
    if name is not None:		# 确认 name 只能是 str 类型, 即 str | None -> str, 窄化了类型范围
        print("Hello, " + name)
```

类型系统还包含两种创建用户自定义类型窄化函数的方式： `typing.TypeIs` 和 `typing.TypeGuard` 。

**TypeIs 和 TypeGuard 其实是函数，返回 True 或 False，都用于判断变量类型能否窄化到目标类型**。

TypeGurad 更灵活（限制更少），比如如下场景：

+ **将类型缩小到不兼容类型，如从 list[object] 到 list[int] 。 TypeIs 仅允许在兼容类型之间进行缩小**

  但是这也可能带来不安全问题。

+ **不对所有缩小类型的输入值返回 True**，比如下面代码，使用 TypeIs 就是错误的写法，但是使用 TypeGurad 是正确的

  ```python
  # 反面案例：
  #   TypeIs 初衷是判断变量是否可以窄化到某个类型，但是这里仅仅正整数会返回True
  #   0 和 负整数明明也可以窄化到 int, 却返回 False
  def is_positive_int(x: object) -> TypeIs[int]:      
      return isinstance(x, int) and x > 0
  # 正面案例：
  def is_positive_int(x: object) -> TypeGurad[int]:
      return isinstance(x, int) and x > 0
  ```

