from ss.configure.blueprint import Blueprint
import re
from typing import Any
from ss.configure.schema import F_ACTION_FLOW


class ActionFlow:
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
        if isinstance(value, str):
            pattern = r"([a-zA-Z_-]+)\.action_flows\.([a-zA-Z_-]+)"
            match = re.match(pattern, value)
            if match is None:
                raise Exception(f"Invalid action value: {value} for action: {name}")

            module, action_flow = match.groups()

            if module in [
                include
                for include, value in blueprint.includes.items()
                if value.get("blueprint")
            ]:
                inner_blueprint = blueprint.includes[module]["blueprint"]
                inner_value = inner_blueprint.action_flows.get(action_flow)

                return self.resolve_unit_action(
                    name=action_flow, value=inner_value, blueprint=inner_blueprint
                )
            else:
                if module in blueprint.units.keys():
                    return self.renderer.render_value(
                        name=name,
                        value=blueprint.units[module]
                        .get("action_flows", {})
                        .get(action_flow),
                        blueprint=blueprint,
                    )
                else:
                    return self.renderer.render_value(
                        name=name, value=value, blueprint=blueprint
                    )
        else:
            return self.renderer.render_value(
                name=name, value=value, blueprint=blueprint
            )
