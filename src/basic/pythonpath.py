"""
1. python src/basic/pythonpath.py 执行以及使用 Code Runner 插件执行会将 py 文件所在目录当作 PYTHONPATH，即 basic
2. python -m src.basic.pythonpath, PYTHONPATH 是 src 所在的目录
3. .vscode/launch.json 启动，如果不通过 .env 选项指定 PYTHONPATH 的话，同1, 即将 py 文件所在目录当作工作目录，
    标准的项目一般将代码文件单独放在代码目录中，所以应该指定 PYTHONPATH
"""

import os
import sys


pythonpath = os.environ.get('PYTHONPATH')
if pythonpath:
    print("环境变量 PYTHONPATH 的值:")
    print(pythonpath)
else:
    print("环境变量 PYTHONPATH 未设置")

print("当前 PYTHONPATH（通过 sys.path 第一项查看）:")
for path in sys.path:
    print("  ", path)
