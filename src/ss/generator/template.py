from abc import ABC, abstractmethod

class Template(ABC):
    @abstractmethod
    def render(self) -> str:
        pass
