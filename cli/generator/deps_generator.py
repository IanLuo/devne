from ..configure.configure import Configure
from .file_generator import FileGenerator

_TEMPLATE_FILE = 'deps.template'
_MARK_DEPS = '#DEPS#'

class DepsGenerator(FileGenerator):
    def __init__(self, configure: Configure):
        self.configure = configure

    def generate(self) -> str:
        with open(_TEMPLATE_FILE, 'r') as f:
            deps_str = f.read()
            return deps_str.replace(_MARK_DEPS, '')
