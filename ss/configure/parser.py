import yaml
from typing import Any, Dict

class Parser:

    def parse_yaml(self, yaml_path: str) -> Dict[str, Any]:
        with open(yaml_path, "r") as f:
            return yaml.load(f, Loader=yaml.FullLoader)


    def parse_unit(self, data: Any) -> Dict[str, Any]:
        def raise_exception(name):
            raise Exception(f"{name} is mandatory")

        if isinstance(data, str):
            return {"source": data}
        elif isinstance(data, dict):
            mandatory = lambda x: data[x] if x in data else raise_exception(x)
            optional = lambda x: data.get(x)

            return {**data, **{
                "source": mandatory("source"),
                "instantiate": optional("instantiate"),
                "actions": optional("actions"),
                "listener": optional("listener"),
            }}
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
        if isinstance(data, str):
            return data

        return '' 


    def parse_action_flow(self, flow: Dict[str, Any]) -> Dict[str, Any]:
        pass


