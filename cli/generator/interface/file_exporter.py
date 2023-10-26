from abc import ABC, abstractmethod

class FileExporter(ABC):
    @abstractmethod
    def export(self):
        pass
