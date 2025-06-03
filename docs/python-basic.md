# Python 基础

## Python 执行原理

### 解释执行流程

![](imgs/python-execution-process.png)

1. **源代码：** 首先，你编写的Python代码被保存为一个文件，其中包含了程序的源代码。
2. **词法分析：** Python解释器会对源代码进行词法分析，将代码分割成一系列的词法单元，如关键字、标识符、运算符等。
3. **语法分析：** 接着，解释器会进行语法分析，将词法单元组织成语法结构。这一步确保代码遵循Python语法规则。
4. **抽象语法树（AST）：** 在语法分析的基础上，解释器生成一个抽象语法树，它表示了代码的结构和逻辑关系。
5. **字节码生成：** 解释器将抽象语法树转换成字节码，这是一种中间形式的代码。字节码并不是直接由计算机硬件执行的机器码，而是由Python解释器执行的一种中间表示。
6. **解释执行：** 解释器根据生成的字节码逐行执行代码。在这个阶段，Python解释器（位于Python虚拟机PVM中，解释器属于PVM的一部分）将代码翻译成机器码并执行相应的操作。这个过程是动态的，即时地执行每一行代码。

> 前5步的流程称为编译（只是编译成字节码.pyc）。
>
> 依赖是在虚拟机中解释执行时加载的。

### 依赖加载流程

和 Java 依赖加载流程类似。也经历了依赖定位、按需导入的流程。不过 Java 依赖包只有字节码，而 Python 可以包含源码文件和字节码文件。

#### 依赖定位

- **搜索路径顺序**：

  1. 当前脚本所在目录

  2. `PYTHONPATH` 环境变量指定的路径

     ```python
     pythonpath = os.environ.get('PYTHONPATH')
     ```

  3. 标准库路径（如 `~/.pyenv/versions/3.12.10`）

  4. `site-packages` 目录（用户安装的第三方包）

  可通过 sys.path 查看完整搜索路径：

  ```python
  import sys
  print(sys.path)
  # 比如
  ['/home/arvin/mywork/python/py-template/src/basic', '/home/arvin/.pyenv/versions/3.12.10/lib/python312.zip', '/home/arvin/.pyenv/versions/3.12.10/lib/python3.12', '/home/arvin/.pyenv/versions/3.12.10/lib/python3.12/lib-dynload', '/home/arvin/.pyenv/versions/3.12.10/lib/python3.12/site-packages']
  ```

+ 模块缓存机制

  首次导入模块时，Python 会：

  1. 编译 `.py` 为 `.pyc` 字节码（存储在 `__pycache__`）
  2. 将模块对象存入 `sys.modules` 字典
  3. 后续导入直接使用缓存。

#### 按需导入（Lazy Import）

+ 静态分析依赖关系

  通过 `import` 语句建立依赖关系，递归递归处理所有导入的模块。

  ```python
  import numpy as np          	# 完全导入
  from pandas import DataFrame 	# 部分导入
  ```

+ 支持动态导入

  程序执行时对导入的包进行导入和移除。

  ```python
  module = __import__('requests')  # 动态导入
  ```

  