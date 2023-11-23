ROOT_FOLDER = 'ss_conf'
CONFIG_FILE = "ss.yaml"
FLAKE_FILE = f'{ROOT_FOLDER}/flake.nix'
UNIT_FILE = f'{ROOT_FOLDER}/units.nix'
FLAKE_METADATA_FILE = f'{ROOT_FOLDER}/flake_metadata.nix'
DEPS_FILE = f'{ROOT_FOLDER}/deps.nix'
DATA_FOLDER = f'{ROOT_FOLDER}/data'

from os.path import exists, dirname, join, abspath
from os import makedirs, path 

class Folder:
    @staticmethod
    def at_current_location(path: str):
        return join(dirname(abspath(__file__)), path)

    @property
    def flake_path(self):
        return f'{self.root}/{FLAKE_FILE}'

    @property
    def unit_path(self):
        return f'{self.root}/{UNIT_FILE}'

    @property
    def flake_metadata_path(self):
        return f'{self.root}/{FLAKE_METADATA_FILE}'

    @property
    def deps_path(self):
        return f'{self.root}/{DEPS_FILE}'

    @property
    def data_folder_path(self):
        return f'{self.root}/{DATA_FOLDER}'

    @property
    def config_path(self):
        return f'{self.root}/{CONFIG_FILE}'

    def __init__(self, root):
        self.root = root

    def init_data_path(self) -> str:
        return self.create_folder(self.data_folder_path)

    def init_flake_file(self):
        return self.make_file(self.flake_path)

    def init_unit_file(self):
        return self.make_file(self.unit_path)

    def init_flake_metadata_file(self):
        return self.make_file(self.flake_metadata_path)

    def init_deps_file(self):
        return self.make_file(self.deps_path)

    def create_folder(self, path):
        if exists(path) == False:
            makedirs(path)

        return path 

    def make_file(self, path, content = ''):
        dir = dirname(path)

        if exists(dir) == False:
            makedirs(dir)

        with open(path, 'w') as f:
            f.write(content)

        return path 

