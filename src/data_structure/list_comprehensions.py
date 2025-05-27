""" List 推导式
https://docs.python.org/3/tutorial/datastructures.html
"""

if __name__ == "__main__":
    result_rows = [
        {'id': 1, 'name': 'Alice'},
        {'id': 2, 'name': 'Bob'}
    ]

    # 使用列表推导式将每一行转换为字典（实际上这里已经是字典了，所以转换不是必需的），最后将所有字典组成一个列表
    # dict() 可以从键值对序列、从映射对象、参数创建字典
    dict_list = [dict(row) for row in result_rows]
    print(dict_list)

    # 取所有姓名值组成一个列表
    name_list = [row['name'] for row in result_rows]
    print(name_list)

    # 使用列表的列表
    pairs = [['a', 1], ['b', 2]]
    d = dict(pairs)
    print(d)

    # 使用元组的列表
    pairs = [('x', 10), ('y', 20)]
    d = dict(pairs)
    print(d)  # 输出: {'x': 10, 'y': 20}
