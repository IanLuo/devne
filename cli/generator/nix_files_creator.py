from .deps_generator import DepsGenerator
from .flake_generator import FlakeGenerator
from .units_generator import UnitsGenerator
from cli.configure.configure import Configure
from cli.folder import Folder
from os.path import exists

class NixFilesCreator:
    def __init__(self, configure: Configure):
        self.deps_generator = DepsGenerator(configure)
        self.flake_generator = FlakeGenerator(configure)
        self.units_generator = UnitsGenerator(configure)
        self.folder = Folder(configure.root)

    def create(self) -> bool:
        try:
        # create config file is not exists
            if not exists(self.folder.config_path):
                self._write_to_file('', self.folder.init_config_file())
                # since the config is just created, the nixs will be not there yet
                return True
    
            # creat flake.nix
            if not exists(self.folder.flake_path):
                self._write_to_file(self.flake_generator.export(), self.folder.init_flake_file())
    
            # create deps.nix
            self._write_to_file(self.deps_generator.export(), self.folder.init_deps_file())
    
            # create unit.nix
            self._write_to_file(self.units_generator.export(), self.folder.init_unit_file())
        except Exception as e:
            print(e)
            return False

        return True

    def _write_to_file(self, content, path):
        with open(path, 'w') as f:
            f.write(content)
