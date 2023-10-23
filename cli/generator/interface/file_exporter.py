from abc import ABC, abstractmethod

class FileExporter:
    @abstractmethod
    def export(self):
        pass
