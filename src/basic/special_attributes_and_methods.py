"""Python 中的特殊属性和方法
    https://docs.python.org/zh-cn/3.13/reference/datamodel.html
    https://docs.python.org/zh-cn/3.13/library/stdtypes.html#special-attributes
    
    __slots__
        __slots__ 允许我们显式地声明数据成员（如特征属性）并禁止创建 __dict__ 和 __weakref__ (除非是在 __slots__ 中显式地声明或是在父类中可用。)
    
    definition.__name__
        类、函数、方法、描述器或生成器实例的名称。

    definition.__qualname__
        类、函数、方法、描述器或生成器实例的 qualified name (限定名称)。
        限定名称：一个以点号分隔的名称，显示从模块的全局作用域到该模块中定义的某个类、函数或方法的路径。
        Added in version 3.3.

    definition.__module__
        类或函数定义所在的模块的名称。

    definition.__doc__
        类或函数的文档字符串，如果未定义则为 None。

    definition.__type_params__
        泛型类、函数和 类型别名 的 类型形参。 对于非泛型类和函数，这将为空元组。    
"""


class C:
    class D:
        def meth(self):
            pass


print(C.__qualname__)
print(C.D.__qualname__)
print(C.D.meth.__qualname__)
