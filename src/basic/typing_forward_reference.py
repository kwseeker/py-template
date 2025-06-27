""" typing 前向引用
详细参考 https://peps.python.org/pep-0563/#forward-references

在模块中故意在名称定义之前使用该名称称为前向引用。在本节的范围内，我们将任何在 if TYPE_CHECKING: 块中导入或定义的名称也称为前向引用。

pep-0563解决了类型提示中的前向引用问题，但是一些仍然需要使用字面量规避前向引用问题的案例：

    <type> 是指某种类型，不是 class type

    类型定义：
    T = TypeVar('T', bound='<type>')
    UserId = NewType('UserId', '<type>')
    Employee = NamedTuple('Employee', [('name', '<type>'), ('id', '<type>')])

    别名：
    Alias = Optional['<type>']
    AnotherAlias = Union['<type>', '<type>']
    YetAnotherAlias = '<type>'
    
    类型转换：
    cast('<type>', value)

    基类：
    class C(Tuple['<type>', '<type>']): ...
"""

# 会让 Python 将所有注解自动保存为字符串，运行时不会尝试解析它们，从而避免前向引用问题
from __future__ import annotations


class Config:
    @classmethod
    # def default(cls, **kwargs) -> 'Config':  # 这里返回值类型提示（Type Hints）涉及前向引用问题，因为此时 Config 类尚未完全定义, 在静态类型检查时会报错，可以使用字面量解决问题
    # 类型提示是静态的，仅在静态类型检查（如 mypy、Pylance）时使用，运行时会被忽略。
    def default(cls, **kwargs) -> Config:   # 引入 __future__ 注解解决
        return Config(**kwargs)     # 这行代码是在运行时才会执行，不会被静态类型检查


c = Config.default()
