# Python VSCode 开发环境配置

## 1 Python 安装（Pyenv）

现在都流行使用**版本管理工具**安装，比如 Java 的 **Jabba**、Node 的 **NVM**，Python 则是 [**Pyenv**](https://github.com/pyenv/pyenv)。

如果用 uv 可以为每个项目单独安装 Python 虚拟环境。

```shell
# 查看安装的python版本和激活的版本
pyenv versions
# 默认会安装到 ~/.pyenv/version 目录下
pyenv install 3.12
pyenv global 3.12
pyenv versions
# 重新加载用户的登录 shell, 会重新读取所有登录时加载的配置文件（如 ~/.bash_profile、~/.zprofile 等），会使上面的操作生效
exec $SHELL -l
python -V
python3 -V
```

pip 安装：

```shell
# Window 中需要在 pip 前加 python -m 
$ pip --version
# 查看已安装的包
$ pip list
# 安装依赖包
# 从PyPI安装 --user 安装到用户安装目录(~/.local/)
$ pip install -U pygame==2.5.1 --user
# 从源码包安装
$ pip install ./pygame
# 从hg上克隆安装
$ pip install hg+https://bitbucket.org/shimizukawa/logfilter
# 通过 requirements.txt 安装
$ pip install -r requirements.txt
$ pip install -U requests 	#更新某个依赖包
# pip 卸载
$ pip uninstall -y flask
```

## 2 VSCode Python 开发环境配置

主要是安装一些插件：

+ Python

+ Pylance

+ Python Snippets

  自动生成常用代码片段。

+ Python Debugger

+ Python Indent

  自动缩进。

+ autoDocstring

  自动生成注释。

+ JetBrains Darcula Theme

  这个主题感觉比较护眼，屏幕看久了也不容易疲劳。

+ autopep8

  按照 PEP8 规范格式化代码。

+ project manager

## 3 包依赖管理工具

### 3.1 [UV](https://github.com/astral-sh/uv)

Rust 编写的超快的新一代依赖管理工具，替代 pip、pdm 等。

[docs](https://docs.astral.sh/uv/)

```shell
# 安装
curl -LsSf https://astral.sh/uv/install.sh | sh
# or
pip install uv
pipx install uv
# 自行更新
uv self update

# uv 初始化项目
uv init example
# 如果需要指定某个Python版本而不是使用当前激活的版本
uv python install 3.8
uv python list 
uv python pin 3.8
uv add xxx
uv remove xxx
# 同步依赖，首次执行会自动创建虚拟环境 .venv
uv sync 
# 创建 lockfile (uv.lock)，记录项目依赖的确切版本，确保在不同环境中能够重现相同的依赖关系
uv lock
# 查看依赖树
uv tree
# 编译并打包, 如果有虚拟环境会使用虚拟环境中的python版本
uv build
uv publish

# 创建虚拟环境， uv sync 会自动创建虚拟环境
uv venv	# 使用当前激活的Python环境
uv venv -p 3.8	# 指定Python版本

# 其他工具
# 显示 uv 安装的 Python 版本路径。
uv python dir

# uv 运行项目
uv run main.py
```

uv 初始化、同步并打包后项目的基本结构:

```shell
.
├── .venv				# 虚拟环境
├── dist				# 编译生成目录
│   ├── .gitignore	
│   ├── mysql_mcp_server-0.1.0-py3-none-any.whl	# Linux 下执行 uv build 打包生成的whl文件，whl默认是作为依赖库，如果项目作为应用项目应该使用后面的应用程序发布流程，比如这个示例项目就不应该打包为 wheel 文件
│   └── mysql_mcp_server-0.1.0.tar.gz			# Linux 下执行 uv build 打包生成的源码包
├── .python-version		# 使用的python版本
├── main.py
├── pyproject.toml
└── uv.lock
```

修改 uv 镜像源：

```toml
# pyproject.toml
[[tool.uv.index]]
url = "https://pypi.tuna.tsinghua.edu.cn/simple"
default = true
```

Python 应用程序发布：

没有找到详细说明应该怎么发布的文档，比如发布到 Docker 镜像，看有的开源项目（Dify）推测是将源码目录拷贝到 Docker 工作目录，直接通过 uv run 等指令解释执行。

比如 Dify Dockfile ：

```shell
WORKDIR /app/api
...
COPY pyproject.toml uv.lock ./
...
# Copy source code
COPY . /app/api/
...
# entrypoint.sh 中通过 flask run ... 启动应用
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
...
ENTRYPOINT ["/bin/bash", "/entrypoint.sh"]
```

另外也可以将应用打包成二进制可执行文件。

## 4 代码格式化

参考：

+ [在 VS Code 中格式化 Python](https://vscode.js.cn/docs/python/formatting)
+ [Formatter extension for Visual Studio Code using autopep8](https://marketplace.visualstudio.com/items?itemName=ms-python.autopep8)

配置好后，按格式化快捷键（Ctrl+Alt+L [这里改为了JetBrain的快捷键], 原始快捷键为 Ctrl+Shift+I）即可格式化Python代码。

**注释风格**：

推荐 Google 的代码风格。

方法注释：

```python
def func(path, field_storage, temporary):
    '''基本描述

    详细描述

    Args:
        path (str): The path of the file to wrap
        field_storage (FileStorage): The :class:`FileStorage` instance to wrap
        temporary (bool): Whether or not to delete the file when the File instance is destructed

    Returns:
        BufferedFileStorage: A buffered writable file descriptor
    '''
    pass
```

类注释：

将Args Returns 替换为 Attibutes 就是类的注释。

## 5 代码调试

参考：[Python debugging in VS Code](https://code.visualstudio.com/docs/python/debugging)

主要关注里面的[配置可选项](https://code.visualstudio.com/docs/python/debugging#_set-configuration-options)。

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: Current File",
            "type": "debugpy",
            // launch: 本地调试 
            // attach: 远程调试
            "request": "launch",
            // 程序入口文件
            // ${file} 指当前激活的文件，即默认调试当前窗口打开的文件
            "program": "${file}",
            // 指定调试器的当前工作目录, 默认为 ${workspaceFolder}， 即 VSCode 打开的文件夹
            "cwd": "${workspaceFolder}",
            // 确保将工作目录作为 PYTHONPATH, 不设置这个的话，会将执行的 py 文件所在目录作为 PYTHONPATH
            // 这个在模块化的工程中也是必设项，除非主文件（比如 main.py）就在 ${workspaceFolder} 根目录下
            "env": {
                "PYTHONPATH": "${workspaceFolder}"  
            },
            // "program": "${workspaceFolder}/src/app.py",
            // integratedTerminal: 在 VSCode 集成终端中执行
            // externalTerminal: 在外部终端中执行
            "console": "integratedTerminal",
            // 添加启动参数 
            //"args" : ["--port", "1593"]
            // 是否仅调试用户的代码, 这个默认是 true, 调试依赖的框架代码时一定要改为 false
            "justMyCode": false
        }
    ]
}
```

调试时读取某个对象字段或变量的值：

可以在 VSCode DEBUG_CONSOLE 窗口输入表达式并回车查看。

**关于各种启动方式下 PYTHONPATH 的默认值** (工程项目推荐后两种方式)：

+ **python + .py 文件路径执行** / **使用 Code Runner 插件执行当前文件**

  会将 .py 文件所在目录当作 PYTHONPATH，比如 python src/basic/pythonpath.py ，即将 basic 作为 PYTHONPATH。

+ **python -m src.basic.pythonpath**

  PYTHONPATH 是 src 所在的目录。

+ **.vscode/launch.json 启动**

  如果不通过 .env 选项指定 PYTHONPATH 的话，同1，即将 py 文件所在目录当作 PYTHONPATH，
  标准的项目一般将代码文件单独放在代码目录中，所以应该指定 PYTHONPATH。

## 6 单元测试

官方标准库提供了 [unittest](https://docs.python.org/zh-cn/3.13/library/unittest.html#)。

单元测试编码规范（从一些优秀的开源项目总结）：

+ 单元测试文件放置到源码根目录下的的专门文件夹，比如 tests；按单元测试、集成测试等划分二级目录；按模块划分三级目录

  ```shell
  tests
  ├── artifact_tests		# 依赖测试
  ├── integration_tests	# 集成测试
  └── unit_tests			# 单元测试
  ```

+ 单元测试源码文件命名以 test_ 开头，应能清楚地反映出它所测试的模块或功能

+ 测试类应该以 Test 开头，不应包含构造函数 `__init__()`

## 7 代码编译与反编译

```shell
# 编译
python -m compileall demo.py
# 直接查看python源码编译会生成的字节码
python -m dis demo.py
# 反编译： 有三种工具（decompile3、uncompile6、pycdc）但是好像对Python新版本支持的都不好
decompyle3 __pycache__/main.cpython-38.pyc
```

Java 使用反编译有一个重要的场景就是理解 Java 中的语法糖实现原理，经过编译和反编译，会将语法糖展现为基础语法实现，使得理解Java 语法糖原理变的很简单。但是对于 Python 貌似不是这样，测试将 Python 装饰器代码编译再反编译语法还是一样，只能从字节码层面理解？

找了下没有找到什么好的方法，基本只能编译成字节码，然后让AI帮忙分析字节码。

## 8 编码规范

官方推荐 [PEP 8](https://peps.python.org/pep-0008/)（Python Enhancement Proposal 8）。

## 9 其他工具或快捷键

+ **查看类的继承关系** -> 类上右键 “Show Type Hierarchy”
+ **查看函数方法的调用链** -> 函数方法上右键 “Show Call Hierarchy” (Ctrl+Alt+H)
