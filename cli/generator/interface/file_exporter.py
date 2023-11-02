from abc import ABC, abstractmethod

class FileExporter(ABC):
    '''complete file content, put the generated content into template'''
    @abstractmethod
    def export(self):
        pass
