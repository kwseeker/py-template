"""Python 重载
https://typing.python.org/en/latest/spec/overload.html

@overload 装饰器允许描述支持多种不同参数类型组合的函数和方法。
这种描述比使用联合更精确，因为联合无法表达参数和返回类型之间的关系

Python 本身不支持真正的函数重载（所有 @overload 定义仅用于类型检查）。只是通过定义多个 @overload 签名声明不同的参数类型组合，最后用一个通用实现处理实际逻辑。

@overload 的意义（感觉是提升了代码的可读性）：
1. @overload 帮助类型检查器理解函数的多种用法，避免类型错误。
2. 自动生成更精确的 API 文档（如 Sphinx 或 IDE 提示）。

无效的重载定义
    1. 至少需要存在两个带 @overload 装饰的定义。如果只有一个，应该报告错误。
    2. 带 @overload 装饰的定义必须后跟一个不带 @overload 装饰的重载实现。类型检查器如果发现实现缺失，应该报告错误或警告。存根文件、协议以及抽象基类中抽象方法内的重载定义不受此检查。
        比如下面的 def parse(self, input: str, *args: Any) -> Union[str, bytes]: ...
    3. 如果一个重载签名被装饰了 @staticmethod 或 @classmethod ，所有重载签名都必须以相同的方式装饰。
    4. 如果为具有重载的函数提供了 @final 或 @override 装饰器，则装饰器应仅应用于重载实现（如果存在）。如果重载实现不存在（例如，在存根文件中），则 @final 或 @override 装饰器应仅应用于第一个重载。
"""

from typing import Any, overload, Union, Optional


class Parser:
    @overload
    def parse(self, input: str) -> str: ...

    @overload
    def parse(self, input: str, encoding: str) -> bytes: ...

    @overload
    def parse(self, input: str, strict: bool, encoding: Optional[str]) -> Union[str, bytes]: ...

    def parse(self, input: str, *args: Any) -> Union[str, bytes]:
        if not args:
            return input.upper()  # 单参数逻辑
        elif len(args) == 1 and isinstance(args[0], str):
            return f"Encoded: {input}".encode(args[0])  # 双参数逻辑
        else:
            if args[0]:  # strict=True
                return input.upper() if args[1] is None else input.encode(args[1])
            return input  # strict=False


# 测试
p = Parser()
print(p.parse("hello"))                  # 输出: "HELLO" (str)
print(p.parse("hello", "utf-8"))         # 输出: b'Encoded: hello' (bytes)
print(p.parse("hello", True, None))      # 输出: "HELLO" (str)
