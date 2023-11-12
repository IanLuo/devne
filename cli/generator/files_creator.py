from .deps_generator import DepsGenerator
from .flake_generator import FlakeGenerator
from .flake_metadata_generator import FlakeMetadataGenerator
from .units_generator import UnitsGenerator
from cli.configure.configure import Configure
from cli.folder import Folder
from os.path import exists

class FilesCreator:
    def __init__(self, configure: Configure):
        self.deps_generator = DepsGenerator(configure)
        self.flake_generator = FlakeGenerator(configure)
        self.flake_metadata_generator = FlakeMetadataGenerator(configure)
        self.units_generator = UnitsGenerator(configure)
        self.folder = Folder(configure.root)

    def create(self) -> bool:
        # creat flake.nix
        if not exists(self.folder.flake_path):
            self._write_to_file(self.flake_generator.export(), self.folder.init_flake_file())

        # create deps.nix
        self._write_to_file(self.deps_generator.export(), self.folder.init_deps_file())

        # create unit.nix
        self._write_to_file(self.units_generator.export(), self.folder.init_unit_file())

        # create metadata.nix
        self._write_to_file(self.flake_metadata_generator.export(), self.folder.init_flake_metadata_file())

        return True

    def _write_to_file(self, content, path):
        with open(path, 'w') as f:
            f.write(content)
