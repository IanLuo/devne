import yaml
from typing import Any, Dict

from ss.configure.schema import K_ACTIONS, K_LISTNER, K_ON_START, K_SOURCE

class Parser:

    def parse_yaml(self, yaml_path: str) -> Dict[str, Any]:
        with open(yaml_path, "r") as f:
            return yaml.load(f, Loader=yaml.FullLoader)


    def parse_unit(self, data: Any) -> Dict[str, Any]:
        def raise_exception(name):
            raise Exception(f"{name} is mandatory")

        if isinstance(data, str):
            return {K_SOURCE: data}
        elif isinstance(data, dict):
            mandatory = lambda x: data[x] if x in data else raise_exception(x)
            optionals = [K_ON_START, K_ACTIONS, K_LISTNER]

            return {**data, 
                    **{ K_SOURCE: mandatory(K_SOURCE) },
                    ** { key: data.get(key) for key in optionals if key in data.keys() }
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
        if isinstance(data, str):
            return data

        return '' 


    def parse_action_flow(self, flow: Dict[str, Any]) -> Dict[str, Any]:
        pass


