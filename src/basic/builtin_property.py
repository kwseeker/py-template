"""@property
@property 用于将方法转换为属性的方式进行访问，常用于封装私有变量或计算属性。
主要是为了安全性方面的考虑，类似 Java 的 private， 让对某个字段的访问仅能通过固定的方法，避免用户错误的使用。
比如下面：
    如果将 _radius 改为 radius 直接允许外部直接访问，用户万一给 radius 传一个负值，这是错误的但是又不会暴露问题，但是通过 def radius(self, value: float) 访问，可以检查值的有效性，更加安全。
"""


class Circle:
    def __init__(self, radius: float):
        self._radius = radius  # 私有变量

    # 读
    @property
    def radius(self) -> float:
        """Getter: 访问半径"""
        return self._radius

    # 写
    @radius.setter
    def radius(self, value: float):
        """Setter: 设置半径（验证合法性）"""
        if value <= 0:
            raise ValueError("半径必须为正数")
        self._radius = value

    @property
    def area(self) -> float:
        """计算属性: 面积（只读）"""
        return 3.14 * self._radius ** 2


# 测试
circle = Circle(5)
print(circle.radius)  # 输出: 5
print(circle.area)    # 输出: 78.5

circle.radius = 10    # 调用 setter
print(circle.area)    # 输出: 314.0
