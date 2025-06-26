"""Pydantic
Pydantic 是使用最广泛的 Python 数据验证库。
"""

from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class BaseEnvironment(BaseModel, extra="forbid"):
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


class Context(BaseModel):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    kwargs: AttrDict = AttrDict()
    config: Config = Field(default_factory=Config.default)


class Environment(BaseEnvironment):
    # model_config = ConfigDict(arbitrary_types_allowed=True)

    desc: str = Field(default="")
    roles: dict[str, SerializeAsAny[BaseRole]] = Field(default_factory=dict, validate_default=True)
    context: Context = Field(default_factory=Context, exclude=True)


class Team(BaseModel):
    # model_config = ConfigDict(arbitrary_types_allowed=True)   # 模型配置可以继承

    env: Optional[Environment] = None
    investment: float = Field(default=10.0)
    idea: str = Field(default="")

    def __init__(self, name, age):
        self.name = name
        self.age = age
