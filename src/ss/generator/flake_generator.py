from ..configure.configure import Configure
from .interface.file_exporter import FileExporter
from .interface.content_generator import ContentGenerator
import os

_FLAKE_TEMPLATE_FILE = 'templates/flake.nix.template'
_MARK_DESCRIPTION = '#DESCRIPTION#'
_MARK_NIXPKGSREV = '#NIXPKGSREV#'

class FlakeGenerator(ContentGenerator, FileExporter):
    def __init__(self, configure: Configure):
        self.configure = configure

    def generate(self) -> dict[str, str]:
        return { k: v for k, v in {
            _MARK_DESCRIPTION: self.configure.description,
            _MARK_NIXPKGSREV: self.configure.nixpkgsrev
        }.items() if v is not None }

    def export(self) -> str:
        return self._generate_flake_file_content()

    def _generate_flake_file_content(self) -> str:
        '''Generate flake.nix file content'''

        current_directory = os.path.dirname(os.path.abspath(__file__))
        metadata_path = os.path.join(current_directory, _FLAKE_TEMPLATE_FILE)

        with open(metadata_path, 'r') as f:
            string = f.read()
            for key, value in self.generate().items():
                string = string.replace(key, str(value))

            return string

