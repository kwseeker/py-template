"""Pydantic
Pydantic 是使用最广泛的 Python 数据验证库。
"""

from typing import Any, Optional
from pydantic import BaseModel, ConfigDict, Field, SerializeAsAny


class BaseEnvironment(BaseModel, extra="forbid"):
    # arbitrary_types_allowed= True ： Pydantic 相信你传进来的是合法的对象，它只做最基础的类型判断，不关心对象里面是什么样子的
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


class C(B):
    p3: float


b = B(p1='hi', p2=2)        # 子类默认没有定义带参数的构造方法，但是从 BaseModel 继承了带参数的构造方法 def __init__(self, /, **data: Any) -> None:
# b = B(p1=12, p2='hi')     # 会校验失败

c = C(p1='hi', p2=2, p3=3.0)    # 且所有子类都可以继承带所有属性的构造方法
print(c)
print(c.p1)

# ----------------
# 子类默认没有定义带参数的构造方法，但是从 BaseModel 继承了带参数的构造方法 def __init__(self, /, **data: Any) -> None:
# Pydantic 通过元类实现了上述功能，这里展示实现原理的模拟，
# 详细参考 Pydantic ModelMetaclass 的实现


class ModelMetaclass(type):
    # 这里的参数名都是有特殊含义的么？
    def __new__(cls, name, bases, namespace):
        # 收集字段注解
        annotations = namespace.get('__annotations__', {})
        for base in bases:
            annotations.update(getattr(base, '__annotations__', {}))
        namespace['_fields'] = annotations

        # 生成 __init__ 并修改类的 __init__ 方法
        def __init__(self, **data: Any):
            for field, type_ in self._fields.items():
                value = data.get(field)
                if not isinstance(value, type_):
                    raise TypeError(f'{field} must be {type_}')
                setattr(self, field, value)
        namespace['__init__'] = __init__

        return super().__new__(cls, name, bases, namespace)


class X(metaclass=ModelMetaclass):
    pass


class Y(X):
    y: int


class Z(Y):
    z: float


z = Z(y=1, z=2.0)   # 默认并不会赋值， BaseModel 是通过元类实现的

print("-------------------")

# -----------------------------------------------
# SerializeAsAny


class User(BaseModel):
    name: str


class UserLogin(User):
    password: str


class OuterModel(BaseModel):
    as_any: SerializeAsAny[User]        # SerializeAsAny[<SomeType>] 会按 <SomeType> 类型进行校验，但是序列化时按 Any 类型序列化
    as_user: User
    user: Any


user = UserLogin(name='pydantic', password='password')
print(OuterModel(as_any=user, as_user=user, user=user).model_dump())
