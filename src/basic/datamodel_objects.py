"""数据模型
对象、值、类型

标准类型

    Callable 类型 （https://docs.python.org/3/reference/datamodel.html#callable-types）
        包括：用户定义的函数、实例方法、生成器函数、协程函数、异步生成器函数、内置函数、内置方法、类、类实例

特殊方法 (https://docs.python.org/3/reference/datamodel.html#special-method-names)：
    object.__new__(cls[, ...])
        调用以创建类 cls 的新实例。 __new__() 是一个静态方法（特殊处理，因此无需声明），它将请求的类的类作为其第一个参数。其余参数是传递给对象构造表达式（对类的调用）的参数。 __new__() 的返回值应该是新的对象实例（通常是 cls 的实例）。
        典型的实现通过使用 super().__new__(cls[, ...]) 调用超类的 __new__() 方法并传入适当的参数来创建类的新的实例，然后在返回之前根据需要对新创建的实例进行必要的修改。
        如果 __new__() 在对象构造期间被调用并且它返回了 cls 的实例，那么新实例的 __init__() 方法将像 __init__(self[, ...]) 一样被调用，其中 self 是新实例，其余参数与传递给对象构造器的参数相同。
        如果 __new__() 没有返回 cls 的实例，那么新实例的 __init__() 方法不会被调用。
        
        ！！！ 使用场景：
        __new__() 主要用于允许不可变类型（如 int、str 或 tuple）的子类自定义实例创建。它也常在自定义元类(MetaClass)中被重写，以自定义类的创建。
        
        类默认会从父类继承 __new__() 方法，最终是从 object 类继承而来。
        
    object.__init__(self[, ...])
        如果基类有一个 __init__() 方法，派生类的 __init__() 方法（如果有），必须显式调用它以确保基类部分的实例正确初始化；例如： super().__init__([args...]) 。
        
    object.__del__(self)
    object.__repr__(self)
    object.__str__(self)
    object.__bytes__(self)
    object.__format__(self, format_spec)
    object.__lt__(self, other)
    object.__le__(self, other)
    object.__eq__(self, other)
    object.__ne__(self, other)
    object.__gt__(self, other)
    object.__ge__(self, other)
    object.__hash__(self)
    object.__bool__(self)
    
    object.__getattr__(self, name)
    object.__getattribute__(self, name)
    object.__setattr__(self, name, value)
    object.__delattr__(self, name)
    object.__dir__(self)
    
    ...
"""


class people:
    # 类属性
    # 如果实例没有 self.name，访问 实例.name 会返回类属性 name（向上查找）。
    # 如果实例有 self.name，访问 实例.name 会返回实例属性（覆盖类属性）。
    # 修改 类名.name 不会影响已经有 self.name 的实例。
    name = ''
    age = 0
    # 类私有属性,私有属性在类外部无法直接进行访问
    __weight = 5

    # 初始化方法
    # python 不支持方法重载, 但是可以使用默认参数来实现类似的功能，带有默认值的参数可以不传入
    def __init__(self, n, a=0):
        self.name = n
        self.age = a

    def speak(self):
        print("%s 说: 我 %d 岁， 体重 %d kg。" % (self.name, self.age, self.__weight))


if __name__ == '__main__':
    p1 = people('张三', 10)
    p2 = people('李四')
    p1.speak()
    p2.speak()
    # print(p.__weight)          # 报错, 类外部无法访问私有属性
    print(p2._people__weight)   # 可以访问
    print(p2.__dict__)          # 可以查看对象的所有属性

print("-------------------------------")

# ----------------------------------------------------
# __new__()
# 子类有重写 __new__() 则创建实例时调用子类重写的方法，没有重写则会调用父类的方法


class A:
    def __new__(cls):
        print("A __new__() called")

    def __init__(self):
        print("A __init__() called")


class B(A):
    # def __new__(cls):
    #     print("B __new__() called")

    def __init__(self):
        print("B __init__() called")


class C:
    """
    If __new__() is invoked during object construction and it returns an instance of cls, then the new instance’s __init__() method will be invoked like __init__(self[, ...]), where self is the new instance and the remaining arguments are the same as were passed to the object constructor.
    """
    # def __new__(cls):               # __new__ 存在时，实例化时不会调用 __init__, 因为这里的  __new__() 没有返回 cls 实例
    #     print("C __new__() called")

    def __init__(self):               # __new__ 不存在时，实例化时会调用 __init__
        print("C __init__() called")


class D:
    name: str = None

    # def __new__(cls, name: str):               # __new__ 存在时，实例化时不会调用 __init__
    #     cls.name = name
    #     print("D __new__() called")

    # def __new__(cls):                          # TypeError: D.__new__() takes 1 positional argument but 2 were given
    #     print("D __new__() called")

    def __init__(self, name: str):               # __new__ 不存在时，实例化时会调用 __init__
        self.name = name
        print("D __init__() called")


a = A()
b = B()
c = C()
d = D("Arvin")
