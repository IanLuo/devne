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

from dataclasses import dataclass
from typing import Dict, Any, Optional
from .parser import parse
import os
import re
import logging
from .lock import Lock
from .nix_resource import NixResource

logging.basicConfig(level=logging.INFO)

@dataclass
class Blueprint:
    units: Dict[str, Any]
    actions: Dict[str, Any]
    action_flows: Dict[str, Any]
    includes: Dict[str, Any]
    metadata: Dict[str, Any]
    include_flakes: Dict[str, Any]
    include_blueprint: Dict[str, 'Blueprint']

    def __init__(self, config_path: str, lock: Optional[Lock] = None):
        self.lock = lock or Lock(config_path)
        self.nix_resource = NixResource(self.lock)
        self.init_blueprint(config_path)

    @property
    def name(self):
        return self.metadata.get("name")

    @property
    def version(self):
        return self.metadata.get("version")

    @property
    def description(self):
        return self.metadata.get("description", "")

    def init_blueprint(self, yaml_path: str):
        logging.info("initializing blueprint..")
        self.include_flakes = {}
        self.include_blueprint = {}

        logging.info(f"parsed blueprint..")
        json = self.parse_yaml(yaml_path)

        logging.info(f"parsed unit..")
        self.units = {
            name: self.parse_unit(data) for name, data in json.get("units", {}).items()
        }
        
        logging.info(f"parsed include..")
        self.includes = {
            name: parse_include(data) for name, data in json.get("include", {}).items()
        }

        logging.info(f"parsed metadata..")
        self.metadata = json.get("metadata", {})

        logging.info(f"parsed actions..")
        self.actions = {
            name: parse_actions(data) for name, data in json.get("actions", {}).items()
        }

        logging.info(f"parsed action flows..")
        self.action_flows = {
            name: parse_action_flow(data)
            for name, data in json.get("action_flows", {}).items()
        }

        logging.info(f"start resolving includes..")
        for name, value in self.includes.items():
            logging.info(f"resolving include '{name}'..")
            self.resolve_include(name, value)

        self.lock.format()

    def resolve_include(self, name: str, value: dict[str, Any]):
        if value is None:
            raise Exception(f"include '{name}' not found")

        nix_store_path = self.collect_include(name, value)

        flake_path = self.nix_resource.find_flake_to_import(nix_store_path)

        if flake_path is not None:
            self.include_flakes[name] = nix_store_path

        ss_path = self.nix_resource.find_ss_to_import(nix_store_path)

        if ss_path is not None:
            self.include_blueprint[name] = Blueprint(ss_path, self.lock)

    def parse_yaml(self, yaml_path: str) -> Dict[str, Any]:
        with open(yaml_path, "r") as f:
            return parse(f)


    def parse_unit(self, data: Dict[str, Any]) -> Dict[str, Any]:
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

    def collect_include(self, name: str, value: Dict) -> str:
        logging.info(f"collecting include {value}..")

        return self.nix_resource.fetch_resource(name, value)


def parse_include(data: Any) -> Dict[str, Any]:
    if isinstance(data, str):
        return {"url": data}
    elif isinstance(data, dict):
        return data
    else:
        raise Exception("include should be a string or a dict")



def parse_actions(data: Any):
    if isinstance(data, str):
        return data

    return '' 


def parse_action_flow(flow: Dict[str, Any]) -> Dict[str, Any]:
    pass


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
    pattern = r'\$(\w*)\.(\w*)'
    match = re.match(pattern, ref)
    if match:
        unit = units.get(match.group(1))
        action = match.group(2)
        return unit, action
    else:
        raise Exception(f'invalid action reference {ref}')


def action_flow(
    action: perform_action):
        pass # TODO:

def perform_condition(param: Any) -> bool:
    pass # TODO:


