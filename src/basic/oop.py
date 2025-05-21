class people:
    # 类属性
    # 如果实例没有 self.name，访问 实例.name 会返回类属性 name（向上查找）。
    # 如果实例有 self.name，访问 实例.name 会返回实例属性（覆盖类属性）。
    # 修改 类名.name 不会影响已经有 self.name 的实例。
    name = ''
    age = 0
    # 类私有属性,私有属性在类外部无法直接进行访问
    __weight = 5

    # 构造方法
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
