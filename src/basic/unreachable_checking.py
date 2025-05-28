"""不可达代码检查
    启用 mypy 的 --warn-unreachable 参数来发现那些你以为会执行但其实不会执行的代码
"""


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
