from ..configure.configure import Configure
from .deps_generator import DepsGenerator
from .units_generator import UnitsGenerator
from .file_generator import FileGenerator

_TEMPLATE_FILE = 'flake.template'

class FlakeGenerator(FileGenerator):
    def __init__(self, configure: Configure):
        self.configure = configure
        self.deps_generator = DepsGenerator(configure)
        self.units_generator = UnitsGenerator(configure)

    def generate(self) -> str:
        return ''

    def write_to_file(self):
        pass


