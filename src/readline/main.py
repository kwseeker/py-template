import atexit
import os
import readline
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme({
    "info": "dim cyan",
    "warning": "magenta",
    "danger": "bold red",
    "success": "bold green",
    "command": "bold yellow",
    "highlight": "bold cyan",
    "agent_name": "bold blue",
    "agent_nick_name": "bold magenta",
    "agent_desc": "green",
    "agent_type": "magenta",
    "tool_name": "bold blue",
    "tool_desc": "green",
    "user_msg": "bold white on blue",
    "assistant_msg": "bold black on green",
})

# Create Rich console object for beautified output
console = Console(theme=custom_theme)

HISTORY_FILE = os.path.expanduser("/tmp/.readline_history")


def _init_readline():
    try:
        # 初始化配置，配置也可以写到配置文件中，通过 readline.read_init_file([filename]) 加载
        # 更多配置项参考 https://tiswww.case.edu/php/chet/readline/readline.html
        # 将 Backspace 绑定为删除前一个单词, \C-? 是终端中 Backspace 键的转义序列
        readline.parse_and_bind(r'"\C-?": backward-kill-word')
        # 将 Delete 键绑定为删除当前字符，\e[3~ 是终端中 Delete 键的转义序列
        readline.parse_and_bind(r'"\e[3~": delete-char')
        # 启用 Emacs 风格的编辑模式
        readline.parse_and_bind('set editing-mode emacs')
        # 输入过长时不换行，而是水平滚动查看
        readline.parse_and_bind('set horizontal-scroll-mode on')
        # 禁止终端响铃
        readline.parse_and_bind('set bell-style none')

        history_dir = os.path.dirname(HISTORY_FILE)
        if not os.path.exists(history_dir):
            os.makedirs(history_dir, exist_ok=True)

        if not os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
                pass

        try:
            # 读取历史记录
            readline.read_history_file(HISTORY_FILE)
        except:
            pass

        # 设置历史记录最大行数
        readline.set_history_length(1000)
        # 禁用当通过 readline 读取输入时对 add_history() 的自动调用
        readline.set_auto_history(False)
        # 程序退出时执行保存历史记录
        atexit.register(_save_history)

    except Exception as e:
        console.print(f"[warning]Failed to initialize command history: {str(e)}[/warning]")


def _save_history():
    """Safely save command history"""
    try:
        readline.write_history_file(HISTORY_FILE)
    except Exception as e:
        console.print(f"[warning]Unable to save command history: {str(e)}[/warning]")


def list_history():
    """List command history"""
    history_length = readline.get_current_history_length()
    if history_length == 0:
        console.print("[info]No command history available.[/info]")
        return

    # console.print("[info]Command History:[/info]")
    for i in range(history_length):
        command = readline.get_history_item(i + 1)
        console.print(f"{i + 1}  [command]{command}[/command]")


def exec_history_cmd(cmd_index: int):
    """List command history"""
    history_length = readline.get_current_history_length()
    if cmd_index < 1 or cmd_index > history_length:
        console.print(f"[warning]Invalid command index: {cmd_index}. Valid range is 1 to {history_length}.[/warning]")
        return

    command = readline.get_history_item(cmd_index)
    exec_cmd(command)


def exec_cmd(command: str) -> bool:
    if command.lower() in {'exit', 'quit'}:
        return True
    elif command.lower() == 'history':
        list_history()
    elif command.lower().startswith('!'):
        exec_history_cmd(int(command[1:].strip()) if command[1:].strip().isdigit() else -1)
    elif command:
        # 处理命令逻辑
        console.print(f"executing command: [command]{command}[/command]")
        readline.add_history(command)
    return False


def main():
    _init_readline()

    clist = {'list', 'pwd', 'clear'}
    for command in clist:
        readline.add_history(command)
    print(f"lines:{readline.get_current_history_length()}")

    should_exit = False
    while not should_exit:
        try:
            command = input("\001\033[1;36m\002CoorAgent>\001\033[0m\002 ").strip()
            se = exec_cmd(command)
            if se:
                should_exit = True
        except EOFError:
            should_exit = True
        except KeyboardInterrupt:
            console.print("[warning]Interrupted by user, exiting...[/warning]")
            should_exit = True


if __name__ == "__main__":
    main()
