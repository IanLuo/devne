import typer
from cli.generator.files_creator import FilesCreator
from cli.configure.configure import Configure
from rich.console import Console
import os 
from typing_extensions import Annotated
from cli.run_command import run

err_console = Console(stderr=True)
std_console = Console()

app = typer.Typer()

@app.command()
def up():
    run('./up')

@app.command()
def update():
    run('./update')

@app.command()
def build(config: str = f'{os.getcwd()}/ss.yaml'):
    name = (Configure(config).name or '').replace(' ', '-')
    version = Configure(config).version or ''
    run(f'./build "./ss_conf#{name}-{version}"')

@app.command()
def init_config(config: str = f'{os.getcwd()}/ss.yaml'):
    '''Run configure wizard to create a config file for your project'''
    Configure.init_default_config(config)

@app.command()
def reload(config: str = f'{os.getcwd()}/ss.yaml'):
    '''re-create all ss related files based on the ss.yaml'''
    Cli(config).reload()

@app.command()
def add_tool(name: Annotated[str, typer.Argument(help='name of the tool')]):
    '''Install a tool for working with the project'''
    pass

@app.command()
def add_dev_dependency(name: str):
    '''this is the documentation'''
    pass

@app.command()
def add_default_dependency(name: str):
    '''this is the documentation'''
    pass

@app.command()
def search_dependency(name: str):
    '''this is the documentation'''
    pass

@app.command()
def search_tool(name: str):
    '''this is the documentation'''
    pass

class Cli:
    def __init__(self, config: str):
        self.configure = Configure(config)

    def reload(self):
        FilesCreator(self.configure).create()

if __name__ == "__main__":
    app()
