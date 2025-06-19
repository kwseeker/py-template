import click
from typing import Optional
import asyncio


@click.group()
@click.pass_context
def cli(ctx: click.Context):
    """命令行工具主入口"""
    ctx.ensure_object(dict)
    ctx.obj['verbose'] = False


@cli.command()
@click.option('-n', '--name', default='World', help='问候的对象')
@click.option('--count', default=1, type=int, help='重复次数')
@click.option('--verbose', is_flag=True, help='详细模式')
@click.pass_context
def greet(ctx: click.Context, name: str, count: int, verbose: bool):
    """简单的问候命令"""
    if verbose:
        click.echo(f"详细模式已启用")
    ctx.obj['verbose'] = verbose

    for i in range(count):
        click.echo(f"Hello, {name}!")


@cli.command()
@click.option('--url', required=True, help='请求的URL')
@click.option('--method', default='GET', help='HTTP方法')
async def fetch(url: str, method: str):
    """异步获取URL内容"""
    click.echo(f"开始异步请求: {method} {url}")
    await asyncio.sleep(1)  # 模拟异步操作
    click.echo(f"请求完成: {url}")


@cli.command()
@click.argument('files', nargs=-1, type=click.Path())
@click.option('--output', '-o', help='输出文件')
def concat(files: list[str], output: Optional[str]):
    """合并多个文件"""
    if not files:
        click.echo("没有提供文件", err=True)
        return

    content = []
    for file in files:
        try:
            with open(file) as f:
                content.append(f.read())
        except IOError:
            click.echo(f"无法读取文件: {file}", err=True)

    if output:
        with open(output, 'w') as f:
            f.write('\n'.join(content))
        click.echo(f"已写入: {output}")
    else:
        click.echo('\n'.join(content))


if __name__ == '__main__':
    cli(obj={})
