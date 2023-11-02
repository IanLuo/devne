from abc import ABC, abstractmethod

class ContentGenerator(ABC):
    ''' only the conent generated '''
    @abstractmethod
    def generate(self) -> dict:
        pass

