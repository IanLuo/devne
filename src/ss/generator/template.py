from abc import ABC, abstractmethod
from ..configure.functions.git_repo import GitRepo
from ..configure.configure import Configure
import re
from typing import Any, Dict


class Template(ABC):
    LINE_BREAK = "\n"

    @abstractmethod
    def render(self) -> str:
        pass

    def _is_path(self, value: str) -> bool:
        return value.startswith("./") or value.startswith("../")

    def _is_var_ref(self, _: Configure, value: str) -> bool:
        pattern = r"^\$([\w\.\_\-]|~>)+$"
        return re.search(pattern, value) is not None

    def render_map(self, configure: Configure, data: Dict[str, Any]) -> str:
        if isinstance(data, dict):
            return f"""
                {{ 
                    {self.LINE_BREAK.join([f'{key} = {self.render_value(configure, value)};' for key, value in data.items() ])
                    } 
                }}
            """
        else:
            raise TypeError("data must be a dictionary")
            

    def render_value(self, configure: Configure, value: Any) -> str:
        if value == None:
            return "nil"
        elif isinstance(value, list):
            return f"""[{self.LINE_BREAK.join(map(lambda x: f'{self.render_value(configure, x)}', value))}]"""
        elif isinstance(value, dict):
            return self.render_map(configure, value)
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, GitRepo):
            return str(value)
        elif isinstance(value, str) and self._is_var_ref(configure, value):
            if value.startswith("$metadata"):
                return value.replace("$", "")
            elif "~>" in value:
                return value.replace("$", "").replace(".", "_").replace("~>", ".")
            else:
                return value.replace("$", "").replace(".", "_") + ".value"
        elif isinstance(value, str) and self._is_path(value):
            return value
        else:
            return f'"{str(value)}"'
