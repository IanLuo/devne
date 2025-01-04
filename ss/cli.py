import json
import os
import subprocess
from typing import Any, List, Optional
import logging

from plumbum import local
from ss.configure.blueprint import Blueprint
from ss.folder import Folder
from ss.generator.files_creator import FilesCreator
from ss.run_command import run
from os.path import dirname, exists
from jsonpath_ng import parse


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
        creator = FilesCreator(
            blueprint=self.blueprint, root=self.root, profile=self.profile
        )
        creator.create_files()

        run(f"nixfmt .ss/ {' '.join(self.folder.all_files('.nix'))}")
        run(f"jsonfmt -w {self.folder.lock_path}")

    @property
    def profile(self) -> dict:
        return self._profile

    @property
    def all_units(self) -> list:
        return list(self.profile.keys())

    def store_path(self, unit: str) -> Optional[str]:
        return self.profile.get(unit)

    def generate_services(self):
        creator = FilesCreator(
            blueprint=self.blueprint, root=self.root, profile=self.profile
        )
        creator.generate_services(blueprint=self.blueprint)

    def list_services(self):
        return [
            service_name
            for unit_name in self.profile.keys()
            for service_name in self.profile.get(unit_name, {})
            .get("services", {})
            .keys()
        ]

    def run_service(self, service_name: str, other_args: List[str], env: dict = {}):
        self.folder.services_path

        if not exists(self.folder.services_path):
            return "No services found"

        else:
            return run(
                f"process-compose -f {self.folder.services_path} run {service_name}"
            )

    def list_actions(self, unit_name: Optional[str] = None):
        if unit_name == None:
            return [
                f"{unit_name}.actions.{action_name}"
                for unit_name in self.profile.keys()
                for action_name in self.profile.get(unit_name, {})
                .get("actions", {})
                .keys()
            ]
        else:
            return [
                f"{unit_name}.actions.{action_name}"
                for action_name in self.profile.get(unit_name, {})
                .get("actions", {})
                .keys()
            ]

    def run_action(
        self, action_name: str, other_args: List[str], env: dict = {}
    ) -> Any:
        jsonpath_expr = parse(f"$.{action_name}")
        match = jsonpath_expr.find(self._profile)

        if not match:
            raise ValueError(f"action {action_name} not found")
        else:
            value = match[0].value

            return self._run_action_value(
                name=action_name, value=value, other_args=other_args, env=env
            )

    def _run_action_value(
        self, name: str, value: Any, other_args: List[str], env: dict = {}
    ):
        if isinstance(value, str):
            return self._run_script_file(
                script_file=value, other_args=other_args, env=env
            )
        elif isinstance(value, list):
            return self._execute_scripts(
                name=name, steps=value, other_args=other_args, env=env
            )
        else:
            raise ValueError(f"Invalid action value: {value} for action: {name}")

    def _run_script_file(self, script_file: str, other_args: List[str], env: dict = {}):
        process = subprocess.Popen(
            [script_file, *(other_args or [])],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env={**os.environ, **env},
        )

        for line in process.stdout:
            yield line.decode("utf-8").strip()

        process.stdout.close()
        process.wait()

        if process.returncode != 0:
            raise subprocess.CalledProcessError(
                process.returncode, script_file, stderr=process.stderr
            )

    def _execute_scripts(
        self, name: str, steps: list, other_args: List[str] = [], env: dict = {}
    ):
        last_output = []

        for current_step in steps:
            index = 0
            for line in self._run_action_value(
                name=name,
                value=current_step,
                other_args=(
                    ["\n".join(last_output)] if len(last_output) > 0 else other_args
                ),
                env=env,
            ):

                if index == 0:
                    last_output = [line]
                else:
                    last_output.append(line)

                index += 1

                yield line
