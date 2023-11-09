from ..configure.configure import Configure
from .interface.content_generator import ContentGenerator
from .interface.file_exporter import FileExporter
import os

_DEPS_TEMPLATE_FILE = './templates/deps.nix.template'
_MARK_DEPS = '#DEPS#'

class DepsGenerator(ContentGenerator, FileExporter):
    def __init__(self, configure: Configure):
        self.configure = configure

    def generate(self) -> dict:
        return { _MARK_DEPS: self._render_deps() }

    def export(self) -> str:
        '''Generate deps.nix file content'''

        current_directory = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_directory, _DEPS_TEMPLATE_FILE)

        with open(path, 'r') as f:
            deps_str = f.read()
            for key, value in self.generate().items():
                deps_str = deps_str.replace(key, value)

            return deps_str

    def _render_deps(self):
        return '\n'.join(self.configure.tools)
