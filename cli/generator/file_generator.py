from abc import ABC, abstractmethod

class FileGenerator(ABC):
    @abstractmethod
    def generate(self) -> str:
        pass

