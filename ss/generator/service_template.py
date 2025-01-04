import logging
from ss.generator.renderer import Renderer
from ss.configure.blueprint import Blueprint
from ss.configure.schema_gen import schema, LINE_BREAK
from json import load
from jsonpath_ng import parse


class ServiceTemplate:
    def __init__(self, blueprint: Blueprint, profile: dict):
        self.renderer = Renderer()
        self.blueprint = blueprint
        self.profile = profile

    def render(self):
        services = self.blueprint.services

        def generate_service(name: str, service: dict):
            command_path = (
                f'{self.blueprint.metadata.get("name")}.services.{name}.command'
            )
            depends_on_path = (
                f'{self.blueprint.metadata.get("name")}.services.{name}.depends-on'
            )

            def extract(key_path: str, json: dict) -> str:
                match = parse(f"$.{key_path}").find(json)

                if len(match) == 0:
                    logging.info(f"no command found for {key_path}")
                    return ""

                return match[0].value

            command = extract(command_path, self.profile)
            depends_on = extract(depends_on_path, self.profile)

            return f"""
            {name}:
                depends_on: {depends_on}
                command: {command}
            """

        return f"""
        processes:
            { LINE_BREAK.join([generate_service(name, service) for name, service in services.items()]) }
        """
