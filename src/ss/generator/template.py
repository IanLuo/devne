from abc import ABC, abstractmethod
from ..configure.functions.git_repo import GitRepo
import re
from typing import Any, Dict


class Template(ABC):
    LINE_BREAK = "\n"
    SYS_SOURCE_NAME = ["pkgs", "ssunits"]

    def filter_sys_sources(self, sources):
        return list(
            filter(lambda source: source in self.SYS_SOURCE_NAME == False, sources)
        )

    @abstractmethod
    def render(self) -> str:
        pass

    def _is_path(self, value: str) -> bool:
        return value.startswith("./") or value.startswith("../")

    def _is_multiple_lines(self, value: str) -> bool:
        return "\n" in value

    def _is_var_ref(self, value: str) -> bool:
        pattern = r"^\$([\w\.\_\-]|~>)+$"
        return re.search(pattern, value) is not None

    def render_map(self, data: Dict[str, Any]) -> str:
        if isinstance(data, dict):
            return f"""
                {{
                    {self.LINE_BREAK.join([f'{key} = {self.render_value(value)};' for key, value in data.items() ])
                    }
                }}
            """
        else:
            raise TypeError("data must be a dictionary")

    def render_value(self, value: Any) -> str:
        if value == None:
            return "null"
        elif isinstance(value, list):
            return f"""[{self.LINE_BREAK.join(map(lambda x: f'{self.render_value(x)}', value))}]"""
        elif isinstance(value, dict):
            return self.render_map(value)
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, GitRepo):
            return str(value)
        elif isinstance(value, str) and self._is_var_ref(value):
            if value.startswith("$metadata"):
                return value.replace("$", "")
            else:
                return value.replace("$", "")
        elif isinstance(value, str) and self._is_path(value):
            return value
        elif isinstance(value, str) and self._is_multiple_lines(value):
            q = "''"
            return f'''
                {q}{value}{q}
            ''' 
        else:
            return f'"{str(value)}"'
