"""Python的特殊参数
https://docs.python.org/3/tutorial/controlflow.html#special-parameters

函数参数定义：
def f(pos1, pos2, /, pos_or_kwd, *, kwd1, kwd2):
      -----------    ----------     ----------
        |             |                  |
        |        Positional or keyword   |
        |                                - Keyword only
         -- Positional only
/ 和 * 是分隔符号，用于区分参数类型。
"""
