"""Pydantic
Pydantic 是使用最广泛的 Python 数据验证库。
"""

from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field


class BaseEnvironment(BaseModel, extra="forbid"):
    # Pydantic 相信你传进来的是合法的对象，它只做最基础的类型判断，不关心对象里面是什么样子的
    model_config = ConfigDict(arbitrary_types_allowed=True)


class AttrDict(BaseModel):
    """A dict-like object that allows access to keys as attributes, compatible with Pydantic."""

    model_config = ConfigDict(extra="allow")

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.__dict__.update(kwargs)

    def __getattr__(self, key):
        return self.__dict__.get(key, None)

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __delattr__(self, key):
        if key in self.__dict__:
            del self.__dict__[key]
        else:
            raise AttributeError(f"No such attribute: {key}")

    def set(self, key, val: Any):
        self.__dict__[key] = val

    def get(self, key, default: Any = None):
        return self.__dict__.get(key, default)

    def remove(self, key):
        if key in self.__dict__:
            self.__delattr__(key)


class Config:
    llm: str

    @classmethod
    def default(cls, **kwargs) -> 'Config':
        return Config(**kwargs)


class Context(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    kwargs: AttrDict = AttrDict()
    # default_factory 是一个 Callable 类型，用于生成默认值
    config: Config = Field(default_factory=Config.default)


class Environment(BaseEnvironment):
    # model_config = ConfigDict(arbitrary_types_allowed=True)

    desc: str = Field(default="")
    # roles: dict[str, SerializeAsAny[BaseRole]] = Field(default_factory=dict, validate_default=True)
    context: Context = Field(default_factory=Context, exclude=True)


class Team(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)   # 模型配置可以继承

    env: Optional[Environment] = None
    investment: float = Field(default=10.0)
    idea: str = Field(default="")

    def __init__(self, context: Context = None, **data: Any):
        # super(Team, self).__init__(**data)
        super().__init__(**data)                # 子类重写 __init__ 后不会自动调用父类的 __init__, 所以这里需要手动调用父类(BaseModel)的 __init__ 执行校验
        ctx = context or Context()
        self.env = Environment(context=ctx)
        self.investment = data['investment']
        self.idea = data['idea']


config = Config.default()
config.llm = "deepseek-chat"
context = Context(config=config)
# context = Context(config={})        # 会校验失败
team = Team(context=context, investment=5, idea="Generate 2048 game")
# team = Team(context=context, investment='ss', idea="Generate 2048 game")    # 会校验失败

print("---------------------------------")

# -----------------------------------------------


class A:
    p1: str
    p2: int


# a = A(p1=12, p2='hi')   # 类默认并没有带参数的构造方法，TypeError: A() takes no arguments


class B(BaseModel):
    p1: str
    p2: int


b = B(p1='hi', p2=2)        # 子类默认没有定义带参数的构造方法，但是从 BaseModel 继承了带参数的构造方法 def __init__(self, /, **data: Any) -> None:
# b = B(p1=12, p2='hi')     # 会校验失败
