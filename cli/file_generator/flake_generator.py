from abc import ABC, abstractmethod
from ..configure.configure import Configure
from deps_generator import DepsGenerator
from units_generator import UnitsGenerator

class FileGenerator(ABC):
    @abstractmethod
    def generate(self) -> str:
        pass

class FlakeGenerator(FileGenerator):
    def __init__(self, configure: Configure):
        self.configure = configure
        self.deps_generator = DepsGenerator(configure)
        self.units_generator = UnitsGenerator(configure)

    def generate(self) -> str:
        return ''

    def write_to_file(self):
        pass


