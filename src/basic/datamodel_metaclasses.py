"""元类（MetaClasses）
    https://docs.python.org/3/reference/datamodel.html#metaclasses
    https://peps.python.org/pep-3115/
    元类即定义类的类。
    
    首先需要理解带三个参数的 type() 和 __new__() 的作用
    
    class type(name, bases, dict, **kwds) 
    返回一个新的类型对象。这本质上是 class 语句的动态形式。名称字符串是类名，并成为 __name__ 属性。基元元组包含基类，并成为 __bases__ 属性；如果为空，则添加 object ，所有类的终极基类。字典字典包含类体的属性和方法定义；它可能在成为 __dict__ 属性之前被复制或包装。
    X = type('X', (), dict(a=1)) 
    等效于
    class X:
        a = 1
        
    
        
"""


class ConfigDict:
    """模拟 Pydantic 的 ConfigDict"""

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        return f"ConfigDict({self.__dict__})"


class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs, **kwargs):
        """
        cls: 元类本身（通常是 ModelMetaclass)
        name: 类名
        bases: 父类列表
        attrs: 类的属性字典
        """
        # 创建类之前，先提取 kwargs 中的配置项
        config_kwargs = kwargs  # 如: extra='ignore', frozen=True

        # 创建类
        new_class = super().__new__(cls, name, bases, attrs)

        # 获取或创建 model_config
        if hasattr(new_class, 'model_config'):
            # 如果已有 model_config，更新它的属性
            for k, v in config_kwargs.items():
                setattr(new_class.model_config, k, v)
        else:
            # 否则创建一个新的 ConfigDict
            new_class.model_config = ConfigDict(**config_kwargs)

        return new_class


class BaseModel(metaclass=ModelMetaclass):
    pass


class MyModel(BaseModel, extra="ignore", frozen=True):      # 这里的 keyword 参数会被传给 ModelMetaclass.__new__() kwargs 参数
    pass


# 测试输出
print(MyModel.model_config)
