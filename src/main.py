import typer
import os 
from typing_extensions import Annotated

from ss.configure.configure import Configure
from ss.generator.files_creator import FilesCreator
from ss.run_command import run
from ss.folder import Folder
from typing import Optional

app = typer.Typer()

def version(value: bool):
    if value:
        import importlib.metadata

        distribution_name = "ss"  # Replace with the actual distribution name

        try:
            version = importlib.metadata.version(distribution_name)
            typer.echo(f"Version: {version}")
        except importlib.metadata.PackageNotFoundError:
            typer.echo(f"Package not found: {distribution_name}")
        finally:
            raise typer.Exit()

@app.callback()
def main(version: Annotated[
         Optional[bool], typer.Option("--version", "-v", callback=version)
         ] = None):
    pass

@app.command()
def up():
    file = Folder.at_current_location('scripts/up')
    os.system(f'bash {file}')

@app.command()
def update():
    run(Folder.at_current_location('scripts/update'))

@app.command()
def build(config: str = f'{os.getcwd()}/ss.yaml'):
    '''build the app based on the ss.yaml'''
    name = (Configure(config).name or '')
    script = Folder.at_current_location('scripts/build') 
    run(f'{script} "./ss_conf#{name}"')

@app.command()
def info():
    run(Folder.at_current_location('scripts/info'))

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
