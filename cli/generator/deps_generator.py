from ..configure.configure import Configure
from .file_generator import FileGenerator
from functools import reduce

class DepsGenerator(FileGenerator):
    def __init__(self, configure: Configure):
        self.configure = configure

    def generate(self) -> str:
        all = self.configure.dependenciesDefault + self.configure.dependenciesDev
        return reduce(lambda last, next: f'{last}\n{next}' ,all)
