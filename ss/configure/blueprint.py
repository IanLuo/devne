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
from .parser import Parser
import os
from os.path import exists
import re
import logging
from ..resources.resource_manager import ResourceManager
from ..folder import Folder
from os.path import dirname, join
from .schema_gen import schema


@dataclass
class Blueprint:
    units: Dict[str, Any]
    actions: Dict[str, Any]
    onstart: Dict[str, Any]
    includes: Dict[str, Any]
    services: Dict[str, Any]
    metadata: Dict[str, Any]
    is_root_blueprint: bool

    def __init__(
        self,
        root: str,
        include_path: Optional[str] = None,
        config_path: Optional[str] = None,
    ):
        self.folder = Folder(root)
        config_path = config_path or self.folder.config_path

        self.parser = Parser()
        self.is_root_blueprint = include_path is None
        self.root = root
        self.gen_folder = Folder(self.folder.data_folder_path or include_path)
        self.config_folder = Folder(dirname(config_path))
        self.resource_manager = ResourceManager(
            lock_root=root, config_folder=self.config_folder
        )

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

        logging.info(f"parsing blueprint..")
        json = self.parser.parse_yaml(yaml_path)

        logging.info(f"parsing unit..")
        self.units = {
            name: self.parser.parse_unit(data)
            for name, data in json.get(schema.units.__str__, {}).items()
        }

        logging.info(f"parsing include..")
        self.includes = {
            name: self.parser.parse_include(data)
            for name, data in json.get(schema.includes.__str__, {}).items()
        }

        logging.info(f"parsing metadata..")
        self.metadata = json.get("metadata", None)
        if self.metadata is None:
            raise Exception("metadata is mandatory")
        elif self.metadata.get("name") is None:
            raise Exception("name is mandatory")

        logging.info(f"parsing actions..")
        self.actions = {
            name: self.parser.parse_actions(data)
            for name, data in json.get(schema.actions.__str__, {}).items()
        }

        logging.info(f"parsing onstart...")
        self.onstart = self.parser.parse_onstart(
            data=json.get(schema.onstart.__str__, [])
        )

        logging.info(f"parsing services...")
        self.services = self.parser.parse_services(
            data=json.get(schema.services.__str__, {})
        )

    def resovle_all_includes(self, includes: Dict[str, Any]):
        logging.info(f"start resolving includes..")
        for name, value in includes.items():
            logging.info(f"resolving include '{name}'..")
            self.resolve_include(name, value)

    def resolve_include(self, name: str, value: dict[str, Any]):
        logging.info(f"collecting include {value}..")
        resource_name = self.metadata.get("name", "") + "-" + name
        include_resource = self.resource_manager.fetch_resource(resource_name, value)

        self.includes[name] = {
            **self.includes[name],
            **include_resource.__dict__,
            "gen_root": self.gen_folder.include_path(name=name),
        }

        ss_path = Folder(include_resource.local_path).config_path

        if exists(ss_path):
            logging.info(f"found ss.yaml at {ss_path}, using it..")
            self.includes[name]["blueprint"] = Blueprint(
                root=self.root,
                include_path=self.gen_folder.include_path(name),
                config_path=ss_path,
            )
