"""列表
list 可以直接通过 + 合并
"""


from dataclasses import dataclass
from typing import Any
from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str = 'user'
    content: str
    send_to: set[str] = Field(default='<all>', validate_default=True)

    def __init__(self, content: str = "", **data: Any):
        data['content'] = data.get('content', content)
        # 类本身并没有通过 keywords 给字段自动赋值的方法，这里是调用的 BaseModel 通过元组实现的通过 keywords 给字段自动赋值的初始化方法
        super().__init__(**data)


class UserMessage(Message):
    def __init__(self, content: str, **kwargs):
        kwargs.pop('role', None)
        super().__init__(content=content, role='user', **kwargs)


user_message = UserMessage(content="some thing", send_to=["Mike"])
print(user_message)     # role='user' content='some thing' send_to={'Mike'}

# list 可以直接通过 + 合并
messages = [user_message] + [UserMessage(content="xxxxxx", send_to=["Mike", "<all>"])]
print(messages)     # role='user' content='some thing' send_to={'Mike'}
