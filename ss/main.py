import json
import typer
from typing_extensions import Annotated
import os
from ss.cli import Cli
from ss.run_command import run
from ss.folder import Folder
from typing import Dict, Optional, Set
import logging
from .run_command import run
from rich.console import Console
from rich.theme import Theme
from typing import List

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


def parse_key_value_pairs(value: str) -> Dict[str, str]:
    if len(value) == 0:
        return {}
    """Parse a comma-separated list of key=value pairs into a dictionary."""
    return dict(item.split("=") for item in value.split(","))


@app.callback(no_args_is_help=True)
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
def units(config: str = default_config):
    """List all units"""
    units = Cli(config).all_units
    console.print(units)


@app.command()
def exec(
    name: str,
    other_args: List[str] = typer.Argument(None),
    env: str = typer.Option(
        "",
        "--env",
        "-e",
        callback=parse_key_value_pairs,
        help="Environment variables, e.g. --env key1=value1,key2=value2",
    ),
    config: str = default_config,
):
    """Execute an action with the given name"""
    for line in Cli(config).run_action(name, other_args=other_args, env=env):
        console.print(line)


if __name__ == "__main__":
    app()
