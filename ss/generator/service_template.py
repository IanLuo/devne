import logging
from ss.configure.blueprint import Blueprint
from ss.configure.schema_gen import schema, LINE_BREAK
from json import load
from jsonpath_ng import parse
import hashlib
import yaml
from os.path import join


class ServiceTemplate:
    def __init__(self, blueprint: Blueprint, profile: dict):
        self.blueprint = blueprint
        self.profile = profile

    def render(self):
        services_path = f'{self.blueprint.metadata.get("name")}.services'
        match = parse(f"$.{services_path}").find(self.profile)
        if len(match) == 0:
            logging.info(f"no services found for {services_path}")
            return ""

        services = match[0].value

        def render_service(name: str, service: dict, all_services: dict):
            def extract(key_path: str, json: dict) -> str:
                match = parse(f"$.{key_path}").find(json)

                if len(match) == 0:
                    logging.info(f"no command found for {key_path}")
                    return None

                return match[0].value

            command_path = f"command"
            depends_on_path = f"depends-on"

            command = extract(command_path, service)
            depends_on = extract(depends_on_path, service)

            if isinstance(depends_on, list):
                depends_on = depends_on
            elif depends_on == None:
                depends_on = []
            else:
                depends_on = [depends_on]

            all_services[name] = {
                "command": command,
                "depends_on": None if len(depends_on) == 0 else
                    { name: { "condition": "process_completed_successfully" } for name in depends_on },
            }

            return all_services

        resolved_services = {
            key: value
            for name, service_dict in services.items()
            for key, value in render_service(
                name=name, service=service_dict, all_services={}
            ).items()
        }

        return yaml.dump(
            {
                "log_level": "info",
                "log_location": join(
                    self.blueprint.gen_folder.path, "log/service/logfile.log"
                ),
                "processes": resolved_services,
            }
        )
