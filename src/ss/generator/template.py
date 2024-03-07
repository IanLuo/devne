from abc import ABC, abstractmethod
from ..configure.functions.git_repo import GitRepo
from ..configure.configure import Configure
import re


class Template(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

    def _is_var_ref(self, configure: Configure, value: str) -> bool:
        pattern = r"^\$[\w\.\_]+$"
        return re.search(pattern, value) is not None

    def render_map(self, configure: Configure, data: dict) -> str:
        line_break = "\n"
        return f"""{{ {line_break.join([ f'{key} = {self.render_value(configure, value)};' for key, value in data.items() ])} }}"""

    def render_value(self, configure: Configure, value) -> str:
        if isinstance(value, list):
            return f"""[{" ".join(map(lambda x: f'"{x}"', value))}]"""
        elif isinstance(value, dict):
            return self._render_map(configure, value)
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, GitRepo):
            return StrRender(
                f"""
                TODO: render git repo
            """
            ).render
        elif None:
            return "nil"
        elif str and self._is_var_ref(configure, value):
            return value.replace("$", "").replace(".", "_")

        else:
            return f'"{str(value)}"'
