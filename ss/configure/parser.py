import yaml
from typing import Any, Dict

from ss.configure.schema_gen import schema


class Parser:

    def parse_yaml(self, yaml_path: str) -> Dict[str, Any]:
        with open(yaml_path, "r") as f:
            return yaml.load(f, Loader=yaml.FullLoader)

    def parse_unit(self, data: Any) -> Dict[str, Any]:
        def raise_exception(name):
            raise Exception(f"{name} is mandatory")

        if isinstance(data, str):
            return {schema.units.source.__str__: data}
        elif isinstance(data, dict):
            mandatory = lambda x, default: data[x] if x in data else default
            optionals = filter(
                lambda x: x != schema.units.source.__str__, schema.pre_defined
            )

            return {
                **data,
                **{
                    schema.units.source.__str__: mandatory(
                        schema.units.source.__str__, "null"
                    )
                },
                **{key: data.get(key) for key in optionals if key in data.keys()},
            }
        else:
            raise Exception("unit should be a string or a dict")

    def parse_include(self, data: Any) -> Dict[str, Any]:
        if isinstance(data, str):
            return {"url": data}
        elif isinstance(data, dict):
            return data
        else:
            raise Exception("include should be a string or a dict")

    def parse_actions(self, data: Any):
        return data

    def parse_onstart(self, data: Any) -> Any:
        if isinstance(data, list):
            return data
        elif isinstance(data, str):
            return data
        else:
            raise Exception("onstart needs to be a string or a list of str")

    def parse_services(self, data: Any):
        return data
