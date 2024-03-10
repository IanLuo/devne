from abc import ABC, abstractmethod
from ..configure.functions.git_repo import GitRepo
from ..configure.configure import Configure
from .str_render import StrRender
import re


class Template(ABC):
    LINE_BREAK = "\n"

    @abstractmethod
    def render(self) -> str:
        pass

    def _is_path(self, value: str) -> bool:
        return value.startswith("./") or value.startswith("../")

    def _is_var_ref(self, configure: Configure, value: str) -> bool:
        pattern = r"^\$([\w\.\_\-]|~>)+$"
        return re.search(pattern, value) is not None

    def render_map(self, configure: Configure, data: dict) -> str:
        return f"""{{ {self.LINE_BREAK.join([ f'{key} = {self.render_value(configure, value)};' for key, value in data.items() ])} }}"""

    def render_value(self, configure: Configure, value) -> str:
        if isinstance(value, list):
            return f"""[{self.LINE_BREAK.join(map(lambda x: f'{self.render_value(configure, x)}', value))}]"""
        elif isinstance(value, dict):
            return self.render_map(configure, value)
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, GitRepo):
            return StrRender(str(value)).render
        elif None:
            return "nil"
        elif str and self._is_var_ref(configure, value):
            if value.startswith("$metadata"):
                return value.replace("$", "")
            elif "~>" in value:
                return value.replace("$", "").replace(".", "_").replace("~>", ".")
            else:
                return value.replace("$", "").replace(".", "_") + ".value"
        elif str and self._is_path(value):
            return value
        else:
            return f'"{str(value)}"'
