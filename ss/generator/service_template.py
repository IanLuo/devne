from ss.generator.renderer import Renderer
from ss.configure.blueprint import Blueprint


class ServiceTemplate:
    def __init__(self, blueprint: Blueprint):
        self.renderer = Renderer()
        self.blueprint = blueprint

    def render(self):
        services = self.blueprint.services

        def generate_service(service: dict):
            f"""

            """

        return f"""
        processes:
            { LINE_BREAK.join([generate_service(service) for service in services]) }
        """
