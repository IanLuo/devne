import typer
from typing_extensions import Annotated
import os
from ss.configure.blueprint import Blueprint
from ss.generator.files_creator import FilesCreator
from ss.run_command import run
from ss.folder import Folder
from typing import Optional
from os.path import dirname
import logging
import json
from jsonpath_ng import parse
from .run_command import run
from rich.console import Console
from rich.theme import Theme

app = typer.Typer()
default_config = f"{os.getcwd()}/ss.yaml"
console = Console(theme=Theme({"info": "cyan", "warning": "yellow", "error": "red"}))


def version(value: bool):
    if value:
        import importlib.metadata

        distribution_name = "ss"  # Replace with the actual distribution name

        try:
            version = importlib.metadata.version(distribution_name)
            console.print(f"Version: {version}")
        except importlib.metadata.PackageNotFoundError:
            console.print(f"Package not found: {distribution_name}")
        finally:
            raise typer.Exit()


@app.callback()
def main(
    version: Annotated[
        Optional[bool], typer.Option("--version", "-v", callback=version)
    ] = None,
    log: Annotated[Optional[str], typer.Option("--log", "-l")] = "WARN",
):
    if log == "INFO":
        logging.basicConfig(level=logging.INFO)
    else:
        logging.basicConfig(level=logging.WARN)


@app.command()
def up():
    file = Folder.at_current_location("scripts/up")
    run(file)


@app.command()
def reload(config: str = default_config):
    """re-create all ss related files based on the ss.yaml"""
    Cli(config).reload()


@app.command()
def actions(
    unit_name: Annotated[Optional[str], typer.Argument()] = None,
    config: str = default_config,
):
    """List all actions or list actions for a specific unit,
    if unit_name is provided
    otherwise show all actions for ss
    """

    actions = Cli(config).list_actions(unit_name)
    console.print(actions)


@app.command()
def action_flows(
    unit_name: Annotated[Optional[str], typer.Argument()] = None,
    config: str = default_config,
):
    """List all action flows or list action flows for a specific unit,
    if unit_name is provided
    otherwise show all action flows for ss
    """
    action_flows = Cli(config).list_action_flows(unit_name)
    console.print(action_flows)


@app.command()
def units(config: str = default_config):
    """List all units"""
    units = Cli(config).all_units
    console.print(units)


@app.command()
def exec(
    name: str,
    source: Annotated[Optional[bool], typer.Option("--source", "-s")] = None,
    config: str = default_config,
):
    """Execute an action with the given name"""
    if source != None:
        show_source = True
    else:
        show_source = False

    Cli(config).run_action(name, show_source=show_source)


@app.command()
def exec_flow(
    name: str,
    config: str = default_config,
):
    """Execute an action flow with the given name"""
    Cli(config).run_action_flow(name)


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

        run(f"nixfmt .ss/ {' '.join(self.folder.all_files('.nix'))}")
        run(f"jsonfmt -w {self.folder.lock_path}")

    @property
    def _all_units(self) -> dict:
        return self._profile

    @property
    def all_units(self) -> list:
        return list(self._all_units.keys())

    def store_path(self, unit: str) -> Optional[str]:
        return self._all_units.get(unit)

    def list_actions(self, unit_name: Optional[str] = None):
        if unit_name == None:
            return [
                f"{unit_name}.actions.{action_name}"
                for unit_name in self._all_units.keys()
                for action_name in self._all_units.get(unit_name, {})
                .get("actions", {})
                .keys()
            ]
        else:
            return [
                f"{unit_name}.actions.{action_name}"
                for action_name in self._all_units.get(unit_name, {})
                .get("actions", {})
                .keys()
            ]

    def list_action_flows(self, unit_name: Optional[str] = None):
        if unit_name == None:
            return [
                f"{unit_name}.actionFlows.{action_flow_name}"
                for unit_name in self._all_units.keys()
                for action_flow_name in self._all_units.get(unit_name, {})
                .get("actionFlows", {})
                .keys()
            ]
        else:
            return [
                f"{unit_name}.actionFlows.{action_flow_name}"
                for action_flow_name in self._all_units.get(unit_name, {})
                .get("actionFlows", {})
                .keys()
            ]

    def run_action(self, action_name: str, show_source: bool = False):
        jsonpath_expr = parse(f"$.{action_name}")
        match = jsonpath_expr.find(self._profile)

        if not match:
            raise ValueError(f"action {action_name} not found")
        else:
            shell_file = match[0].value
            if show_source:
                with open(shell_file) as f:
                    print(f.read())
            os.system(f"source {shell_file}")

    def run_action_flow(self, action_flow_name: str):
        jsonpath_expr = parse(f"$.{action_flow_name}")
        match = jsonpath_expr.find(self._profile)

        if not match:
            raise ValueError(f"action flow {action_flow_name} not found")
        else:
            files = match[0].value
            for i, file in enumerate(files):
                if i == 0:
                    os.system(f"source {file} > /tmp/ss_result")
                else:
                    with open("/tmp/ss_result", "r") as f:
                        prev_result = f.read().strip()
                    os.system(f"source {file} {prev_result} > /tmp/ss_result")
                    console.print(f"cat /tmp/ss_result")

            with open("/tmp/ss_result", "r") as f:
                final_result = f.read().strip()
            if final_result:
                print(final_result)
            os.remove("/tmp/ss_result")


if __name__ == "__main__":
    app()
