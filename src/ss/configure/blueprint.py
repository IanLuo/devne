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
6. value
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
from typing import List, Dict, Any
from .parser import parse


@dataclass
class Blueprint:
    units: Dict[str, Any]
    actions: Dict[str, Any]
    action_flows: Dict[str, Any]
    includes: Dict[str, Any]
    metadata: Dict[str, Any]

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


def parse_actions(data: Dict[str, Any]):
    if isinstance(data, str):
        return {"sh": data}

    return {}


def parse_action_flow(flow: Dict[str, Any]) -> Dict[str, Any]:
    pass


#


def perform_condition(param: Any) -> bool:
    pass


def perform_action(
    unit: Dict[str, Any], param: Any, condition: perform_condition = None
) -> Any:
    pass


def action_flow(
    unit1: Dict[str, Any],
    param: Any,
    unit2: Dict[str, Any],
    condition: perform_condition = None,
):
    perform_action(unit2, perform_action(unit1, param), condition)


def listener(condition: perform_condition = None):
    pass
