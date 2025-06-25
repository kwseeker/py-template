"""Typer 
Typer 是一个用于构建 CLI 应用程序的库

Tutorial: https://typer.tiangolo.com/tutorial/
GitHub Repo: https://github.com/fastapi/typer
"""
import typer

# add_completion 自动补全选项（此选项用于自动补全命令、选项信息）--install-completion
# pretty_exceptions_show_locals 控制是否在命令执行出错时显示局部变量（local variables）的信息。当你设置为 True 时，在抛出异常时，Typer 会在错误信息中展示当前函数内的局部变量，帮助调试。
# app = typer.Typer(add_completion=False, pretty_exceptions_show_locals=False)
app = typer.Typer(pretty_exceptions_show_locals=False)


@app.command(help="Greet a person by name.")
def hello(
    name: str = typer.Argument(None, help="The name of the person to greet.")
):
    if name is None:
        typer.echo("Missing argument 'name'.")
        raise typer.Exit()

    print(f"Hello {name}")


@app.command(help="Say goodbye to a person by name.")
def goodbye(
    name: str = typer.Argument(None, help="The name of the person to say goodbye to."),
    formal: bool = typer.Option(False, "--formal", "-f", help="Use formal goodbye greeting.")
):
    """
        uv run src/typer/main.py goodbye Arvin -f
    """
    if formal:
        print(f"Goodbye Ms. {name}. Have a good day.")
    else:
        print(f"Bye {name}!")


if __name__ == "__main__":
    app()
