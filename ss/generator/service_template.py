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
            key_path = f'{self.blueprint.metadata.get("name")}.services.{name}'
            command_path = (
                f'{self.blueprint.metadata.get("name")}.services.{name}.command'
            )

            jsonpath_expr = parse(f"$.{command_path}")
            match = jsonpath_expr.find(self.profile)

            if len(match) == 0:
                logging.info(f"no command found for {command_path}")
                return ""

            command = match[0].value

            return f"""
            {name}:
                depends_on: {service.get("depends_on", '')}
                command: {command}
            """

        return f"""
        processes:
            { LINE_BREAK.join([generate_service(name, service) for name, service in services.items()]) }
        """
