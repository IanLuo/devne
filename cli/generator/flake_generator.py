from ..configure.configure import Configure
from .deps_generator import DepsGenerator
from .units_generator import UnitsGenerator
from .file_generator import FileGenerator
from .units_generator import UnitsGenerator
from .units_ref_generator import UnitsRefGenerator
import os

_TEMPLATE_FILE = 'templates/flake.nix.template'
_DEPS_TEMPLATE_FILE = './templates/deps.nix.template'
_UNITS_TEMPLATE_FILE = 'templates/units.nix.template'
_MARK_UNITS = '#UNITS#'
_MARK_UNITS_REF = '#UNITS_REF#'
_MARK_DEPS = '#DEPS#'


class FlakeGenerator(FileGenerator):
    def __init__(self, configure: Configure):
        self.configure = configure
        self.deps_generator = DepsGenerator(configure)
        self.units_generator = UnitsGenerator(configure)
        self.units_ref_generator = UnitsRefGenerator(configure)

    def generate(self) -> str:
        return ''

    def write_to_file(self):
        pass

    def _generate_units_file(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_directory, _UNITS_TEMPLATE_FILE)
        with open(path, 'r') as f:
            template = f.read()
            result = template.replace(_MARK_UNITS, self.units_generator.generate())
            return result.replace(_MARK_UNITS_REF, self.units_ref_generator.generate())

    def _generate_deps_file(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_directory, _DEPS_TEMPLATE_FILE)

        with open(path, 'r') as f:
            deps_str = f.read()
            return deps_str.replace(_MARK_DEPS, self.deps_generator.generate())

