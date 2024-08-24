import typer
import os
from typing_extensions import Annotated

from ss.configure.blueprint import Blueprint
from ss.generator.files_creator import FilesCreator
from ss.run_command import run
from ss.folder import Folder
from typing import Optional
from os.path import dirname
import logging
import json
from jsonpath_ng import parse

app = typer.Typer()
default_config = f"{os.getcwd()}/ss.yaml"



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
def main(
    version: Annotated[
        Optional[bool], typer.Option("--version", "-v", callback=version)
    ] = None,
    
    log: Annotated[
        Optional[str], typer.Option("--log", "-l")
    ] = 'WARN' 
):
    if log == 'INFO':
        logging.basicConfig(level=logging.INFO)  
    else:
        logging.basicConfig(level=logging.WARN)

@app.command()
def up():
    file = Folder.at_current_location("scripts/up")
    os.system(f"bash {file}")


@app.command()
def update():
    run(Folder.at_current_location("scripts/update"))

@app.command()
def info():
    run(Folder.at_current_location("scripts/info"))


@app.command()
def reload(config: str = default_config):
    """re-create all ss related files based on the ss.yaml"""
    Cli(config).reload()

@app.command()
def actions(unit_name: Annotated[Optional[str], typer.Argument()] = None,
           config: str = default_config):
    '''List all actions or list actions for a specific unit,
    if unit_name is provided
    otherwise show all actions for ss
    '''

    actions = Cli(config).list_actions(unit_name)
    typer.echo(actions)
    
@app.command()
def units(config: str = default_config):
    '''List all units
    '''
    units = Cli(config).all_units
    typer.echo(units)

    
@app.command()
def exec(name: str, 
         source: 
            Annotated[
                Optional[bool], typer.Option("--source", "-s")
            ] = None,
         config: str = default_config):
    '''Execute an action with the given name
    '''
    if source != None:
        show_source = True
    else:
        show_source = False 

    Cli(config).run_action(name, show_source=show_source)

class Cli:
    def __init__(self, config_path: str):
        self.root = dirname(config_path)
        self.blueprint = Blueprint(root=self.root)
        self.folder = Folder(self.root)

    @property
    def _profile(self) -> dict:
        json_str = run("load_profile")
        return json.loads(json_str)

    def reload(self):
        creator = FilesCreator(self.blueprint, self.root)
        creator.create_all()

        os.system(f"nixfmt .ss/ {' '.join(self.folder.all_files('.nix'))}")
        os.system(f'jsonfmt -w {self.folder.lock_path}')

    @property
    def _all_units(self) -> dict:
        return self._profile
        

    @property
    def all_units(self) -> list:
        return list(self._all_units.keys())

    def store_path(self, unit: str) -> Optional[str]:
        return self._all_units.get(unit)
    
    def list_actions(self, 
                    unit_name: Optional[str] = None):
        if unit_name == None:
            return [f'{unit_name}.actions.{action_name}' 
                for unit_name in self._all_units.keys()
                for action_name in self._all_units.get(unit_name, {}).get('actions', {}).keys() 
            ]
        else:
            return [f'{unit_name}.actions.{action_name}' for action_name in self._all_units.get(unit_name, {}).get('actions', {}).keys()]

    def run_action(self, action_name: str, show_source: bool = False):
        jsonpath_expr = parse(f'$.{action_name}')
        match = jsonpath_expr.find(self._profile)

        if not match:
            raise ValueError(f"action {action_name} not found")
        else:
            shell_file = match[0].value
            if show_source:
                with open(shell_file) as f:
                    print(f.read())
            os.system(f"source {shell_file}")


if __name__ == "__main__":
    app()
