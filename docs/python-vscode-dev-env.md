# Python VSCode 开发环境配置

## Python 安装（Pyenv）

现在都流行使用**版本管理工具**安装，比如 Java 的 **Jabba**、Node 的 **NVM**，Python 则是 [**Pyenv**](https://github.com/pyenv/pyenv)。

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

## VSCode Python 开发环境配置

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

## 包依赖管理工具

### [UV](https://github.com/astral-sh/uv)

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
uv add xxx
uv remove xxx
# 同步依赖，首次执行会自动创建虚拟环境 .venv
uv sync 
# 创建 lockfile 
uv lock
# 查看依赖树
uv tree
# 编译并打包
uv build
uv publish

# 创建虚拟环境
uv venv

# 其他工具
# 显示 uv 安装的 Python 版本路径。
uv python dir
```

