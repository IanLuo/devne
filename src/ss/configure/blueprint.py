"""
a blueprint contains:
1. all units that can be used in the project
2. add defined action flows

units includes all resolved from current and included blueprints,
if a unit is defined in the current blueprint, it will override the included one

a unit contains below attributes:
1. name
2. version
3. initialize script (optional)
4. actions
5. source (nipkgs, git, plain text, file, etc)
7. listner (optional)

a action flow is formed as:
(unit1, param, condition?) -> (result) ...
an action flow is basicall a unit action call followd by another action call, whill a optional condition provide,
with the last action call return value is provided as parameter

any executables can be attached to a listener,
if a unit is attached to a lisenter, the unit will be executed (asynchromizely) with the value for the lisenter
and the same for action flow

include supports:
1. ss bluprint: ss.yaml
   if there is a ss.yaml in the destination, use it
2. flake.nix or default.nix
    if a flake or a default.nix is there, use it, and wrap the package in side
    unit

"""

from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional
from .parser import parse
import os
import re
from ..run_command import run

@dataclass
class Blueprint:
    units: Dict[str, Any]
    actions: Dict[str, Any]
    action_flows: Dict[str, Any]
    includes: Dict[str, Any]
    metadata: Dict[str, Any]
    include_flakes: Dict[str, Any]
    include_blueprint: Dict[str, 'Blueprint']

    def __init__(self, config: str):
        self.init_blueprint(config)

    @property
    def name(self):
        return self.metadata.get("name")

    @property
    def version(self):
        return self.metadata.get("version")

    @property
    def description(self):
        return self.metadata.get("description", "")

    def init_blueprint(self, yaml: str):
        self.include_flakes = {}
        self.include_blueprint = {}

        json = parse_yaml(yaml)
        self.units = {
            name: parse_unit(data) for name, data in json.get("units", {}).items()
        }
        
        self.includes = {
            name: parse_include(data) for name, data in json.get("include", {}).items()
        }

        self.metadata = json.get("metadata", {})

        self.actions = {
            name: parse_actions(data) for name, data in json.get("actions", {}).items()
        }

        self.action_flows = {
            name: parse_action_flow(data)
            for name, data in json.get("action_flows", {}).items()
        }

        for name, value in self.includes.items():
            self.resolve_include(name, value)

    def resolve_include(self, name: str, value: dict[str, Any]):
        if value is None:
            raise Exception(f"include '{name}' not found")

        store_path = collect_include(value)

        flake_path = find_flake_to_import(store_path)

        if flake_path is not None:
            self.include_flakes[name] = store_path

        ss_path = find_ss_to_import(store_path)

        if ss_path is not None:
            with open(ss_path, "r") as f:
                self.include_blueprint[name] = Blueprint(f.read())


def parse_yaml(yaml: str) -> Dict[str, Any]:
    return parse(yaml)


def parse_unit(data: Dict[str, Any]) -> Dict[str, Any]:
    def raise_exception(name):
        raise Exception(f"{name} is mandatory")

    mandatory = lambda x: data[x] if x in data else raise_exception(x)
    optional = lambda x: data.get(x)

    return {
        "source": mandatory("source"),
        "instantiate": optional("instantiate"),
        "actions": optional("actions"),
        "listener": optional("listener"),
    }


def parse_include(data: Any) -> Dict[str, Any]:
    if isinstance(data, str):
        return {"url": data}

    return {}


def parse_actions(data: Any):
    if isinstance(data, str):
        return data

    return '' 


def parse_action_flow(flow: Dict[str, Any]) -> Dict[str, Any]:
    pass


# handle include
def find_flake_to_import(store_path: str) -> Optional[str]:
    flake_path = os.path.join(store_path, "flake.nix")

    if os.path.exists(flake_path):
        return flake_path
    else:
        return None

def find_ss_to_import(store_path: str) -> Optional[str]:
    ss_path = os.path.join(store_path, "ss.yaml")

    if os.path.exists(ss_path):
        return ss_path

    return None


def collect_include(value: Any) -> str:
    if isinstance(value, str):
        return fetch_resource(value)
    elif isinstance(value, dict):
        url = value.get("url") 

        if url is None:
            raise Exception("url is mandatory for include")

        return fetch_resource(url)

    else:
        raise Exception("include value should be a string or a dict")


def fetch_resource(url: str) -> str:
    resolved_url = resovle_resource_url(url)
    command = command_for_url(resolved_url)
    result = run(command) or ''

    pattern = r'(/nix/store/[^"]+)'
    match = re.search(pattern, result)
    if match:
        return match.group(1)
    else:
        raise Exception(f'failed to fetch resource from {url}')

# perform actions

def perform_action(
    actions: Dict[str, Any], 
    units: Dict[str, Any], 
    action: str
) -> Any:
    command = actions.get(action)

    if command is None:
        raise Exception(f'command for \'{action}\' not found') 

    if command.startswith("$"):
        unit, unit_action = read_action_ref(command, units)
        perform_action(unit.get('actions', {}), units, unit_action)
    else:
       command = actions.get(action) 
       os.system(f'bash {command}')


def read_action_ref(ref: str, 
                    units: Dict[str, Any] 
) -> tuple[Dict[str, Any], str]:
    pattern = '\$(\w*)\.(\w*)'
    match = re.match(pattern, ref)
    if match:
        unit = units.get(match.group(1))
        action = match.group(2)
        return unit, action
    else:
        return None, None


def action_flow(
    action: perform_action):
        pass # TODO:

def perform_condition(param: Any) -> bool:
    pass # TODO:

def command_for_url(url: str) -> str:
    if url.startswith("path://"):
        return f'nix-instantiate --eval --json -E "fetchTree {url}"'
    else:
        return f'nix-prefetch-url --unpack --print-path {url}'

def resovle_resource_url(url: str) -> str:
    pattern = r'(?P<scheme>\w+)\:(?P<path>\/?.+\/?)'
    matchs = re.match(pattern, url)

    if matchs is None:
        return url

    scheme = matchs.group("scheme") or ''
    path = matchs.group("path")

    def get_nth_element(arr, n):
        return arr[n] if n < len(arr) else None

    if scheme == "github":
        comps = [ comp for comp in path.split("/") if comp != '' ]
        owner = get_nth_element(comps, 0)
        repo = get_nth_element(comps, 1)
        branch = get_nth_element(comps, 2) or 'master'

        return f'https://github.com/{owner}/{repo}/archive/{branch}.tar.gz'

    elif scheme == "path":
        return f'path://{path}'

    else:
        return url
