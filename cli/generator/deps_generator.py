from ..configure.configure import Configure
from .file_generator import FileGenerator
from functools import reduce
import os

_TEMPLATE_FILE = './templates/deps.nix.template'
_MARK_DEPS = '#DEPS#'

class DepsGenerator(FileGenerator):
    def __init__(self, configure: Configure):
        self.configure = configure

    def generate(self) -> str:
        current_directory = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_directory, _TEMPLATE_FILE)

        with open(path, 'r') as f:
            deps_str = f.read()
            return deps_str.replace(_MARK_DEPS, self._read_dependencies(self.configure))

    def _read_dependencies(self, configure: Configure) -> str:
        all = configure.dependenciesDefault + configure.dependenciesDev
        return reduce(lambda last, next: f'{last}\n{next}' ,all)
