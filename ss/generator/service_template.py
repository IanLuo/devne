import logging
from ss.generator.renderer import Renderer
from ss.configure.blueprint import Blueprint
from ss.configure.schema_gen import schema, LINE_BREAK
from json import load
from jsonpath_ng import parse
import hashlib


class ServiceTemplate:
    def __init__(self, blueprint: Blueprint, profile: dict):
        self.renderer = Renderer()
        self.blueprint = blueprint
        self.profile = profile

    def render(self):
        services_path = f'{self.blueprint.metadata.get("name")}.services'
        match = parse(f"$.{services_path}").find(self.profile)
        if len(match) == 0:
            logging.info(f"no services found for {services_path}")
            return ""

        services = match[0].value

        def resolve_service(name: str, service: dict, all_services: dict):
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

            if depends_on is not None:
                depends_on_name = hashlib.md5(str(depends_on).encode()).hexdigest()
                if depends_on_name is not None:
                    all_services.append(
                        {
                            "name": name,
                            "command": command,
                            "depends-on": depends_on_name,
                        }
                    )

                    return resolve_service(
                        name=depends_on_name,
                        service=depends_on,
                        all_services=all_services,
                    )
            else:
                all_services.append(
                    {
                        "name": name,
                        "command": command,
                    }
                )
                return all_services

        def render_service(service: dict):
            return f"""
                {service.get('name')}:
                    depends_on: {service.get('depends-on', '')}
                    command: {service.get('command')}

                """

        resolved_services = [
            service
            for name, service_dict in services.items()
            for service in resolve_service(
                name=name, service=service_dict, all_services=[]
            )
        ]

        return f"""
        processes:
            { LINE_BREAK.join([render_service(service) for service in resolved_services]) }
        """
