"""Python 数字计算
    Python 数字类型有3中 int、float、complex
"""

if __name__ == "__main__":
    list = [1, 2.0, 3.5, 4]
    sum = list[0] + list[1] + list[2] + list[3]
    print(f"type of sum: {type(sum)}")      # sum 是 float， 可以进行自动类型转换
    print(f"sum: {sum}")

    # 除法运算不管是否能够整除都会转成 float
    print(f"3 / 2 = {3 / 2}, type: {type(3/2)}")
    print(f"4 / 2 = {4 / 2}, type: {type(4/2)}")
