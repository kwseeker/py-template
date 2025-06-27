"""内置函数
https://docs.python.org/3/library/functions.html#built-in-functions

S: 
    super(): 
        https://docs.python.org/3/library/functions.html#super
        https://peps.python.org/pep-3135/
        返回一个代理对象，将方法调用委托给 type 的父类或兄弟类。这对于访问在类中被重写的继承方法很有用。
        super() 等同于 super(ParentCls, self)
"""


class Basic:
    name: str = ""

    def __init__(self, name: str):
        self.name = name
        print("Basic init")

    def desc(self):
        print("Basic desc()")


class SubCls(Basic):
    extra: str = ""

    # def __init__(self, name: str, extra: str):
    #     super().__init__(name)
    #     self.extra = extra
    #     print("SubCls init")

    def desc(self):
        super().desc()          # 通过 super() 代理，调用父类方法
        print("SubCls desc()")

    def content(self):
        print(f"name: {self.name}, extra: {self.extra}")


# sco = SubCls("Arvin", "...")  # 子类重写 __init__ 后默认并不会调用父类的 __init__ 方法， 可以通过 super().__init__() 调用父类的初始化方法，其他方法同理
sco = SubCls("Arvin")           # 子类未重写 __init__ 会调用父类的 __init__ 方法
sco.desc()
sco.content()

print("------------------------------")

# -----------------------------------------------------------


class A:
    def __init__(self):
        print("A init")


class B(A):
    def __init__(self):
        super().__init__()
        print("B init")


class C(A):
    def __init__(self):
        super().__init__()
        print("C init")


class D(B, C):
    def __init__(self):
        super().__init__()
        print("D init")


d = D()
