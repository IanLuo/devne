from .deps_generator import DepsGenerator
from .flake_generator import FlakeGenerator
from .sdk_generator import SdkGenerator
from .units_generator import UnitsGenerator
from typing import List

class NixFilesExportor:
    def __init__(self, configure):
        self.deps_generator = DepsGenerator(configure)
        self.flake_generator = FlakeGenerator(configure)
        self.units_generator = UnitsGenerator(configure)
        self.sdk_generator = SdkGenerator(configure)

    def export(self) -> List[str]:
        return []

    def _write_to_file(self, content, path):
        with open(path, 'w') as f:
            f.write(content)
