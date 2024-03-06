from abc import ABC, abstractmethod


class Template(ABC):
    @abstractmethod
    def render(self) -> str:
        pass

    def renderValue(self, value) -> str:
        if isinstance(value, list):
            return f"""[{" ".join(map(lambda x: f'"{x}"', value))}];"""
        elif isinstance(value, dict):
            return self._render_map(value)
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, GitRepo):
            return str(value)
