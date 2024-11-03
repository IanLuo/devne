from ss.configure.blueprint import Blueprint
import re
from typing import Any


class Action:
    def __init__(self, name: str, value: str, blueprint: Blueprint, renderer: Any):
        self.name = name
        self.value = value
        self.blueprint = blueprint
        self.renderer = renderer

    def render(self):
        return self.resolve_unit_action(
            name=self.name, value=self.value, blueprint=self.blueprint
        )

    def resolve_unit_action(self, name: str, value: Any, blueprint: Blueprint):
        return self.renderer.render_value(
            name=name, value=value, blueprint=blueprint, string_as_nix_code=True
        )
