from ..configure.configure import Configure
from .interface.file_exporter import FileExporter
from .interface.content_generator import ContentGenerator
import os

_FLAKE_TEMPLATE_FILE = 'templates/flake.nix.template'

_MARK_NAME = '#NAME#'
_MARK_VERSION = '#VERSION#'
_MARK_DESCRIPTION = '#DESCRIPTION#'

class FlakeGenerator(ContentGenerator, FileExporter):
    def __init__(self, configure: Configure):
        self.configure = configure

    def generate(self) -> dict:
        return { k: v for k, v in { 
            _MARK_NAME: self.configure.name,           
            _MARK_VERSION: self.configure.version,
            _MARK_DESCRIPTION: self.configure.description
        }.items() if v is not None }

    def export(self) -> str:
        return self._generate_flake_file_content()

    def _generate_flake_file_content(self) -> str:
        '''Generate flake.nix file content'''

        current_directory = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_directory, _FLAKE_TEMPLATE_FILE)

        with open(path, 'r') as f:
            str = f.read()
            for key, value in self.generate().items():
                str = str.replace(key, value)

            return str

