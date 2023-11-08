import typer
from cli.generator.files_creator import FilesCreator
from cli.configure.configure import Configure
from rich.console import Console
import os 

err_console = Console(stderr=True)
std_console = Console()

def main(action: str, config: str = f'{os.getcwd()}/ss.yaml'):
    if action == 'init_config':
        Configure.init_empty_config(config)
    elif action == 'help':
       std_console.print('''
    Actions
    - show all actions
    - init_config: create an empty config file
    - reload: reload all dependencies based on your [yellow]ss.yaml[/yellow] file
           ''')
    elif action == 'reload':
        Cli(config).reload()
    else:
        err_console.print(f'action [bold red]\'{action}\'[/bold red] not found')

class Cli:
    def __init__(self, config: str):
        self.configure = Configure(config)

    def reload(self):
        FilesCreator(self.configure).create()

if __name__ == "__main__":
    typer.run(main)
