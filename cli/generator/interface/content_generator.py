from abc import ABC, abstractmethod

class ContentGenerator(ABC):
    @abstractmethod
    def generate(self) -> dict:
        pass

