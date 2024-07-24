ROOT_FOLDER = '.ss'
CONFIG_FILE = "ss.yaml"
LOCK_FILE = "ss.lock"
FLAKE_FILE = f'{ROOT_FOLDER}/ss.nix'
UNIT_FILE = f'{ROOT_FOLDER}/units.nix'
DATA_FOLDER = f'{ROOT_FOLDER}/data'
INCLUDES_FOLDER = f'{ROOT_FOLDER}/includes'

from os.path import exists, dirname, join, abspath
from os import makedirs 

class Folder:
    def __init__(self, root):
        self.root = root

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
    def data_folder_path(self):
        return f'{self.root}/{DATA_FOLDER}'

    @property
    def config_path(self):
        return f'{self.root}/{CONFIG_FILE}'

    @property
    def lock_path(self):
        return f'{self.root}/{LOCK_FILE}'

    def init_data_path(self) -> str:
        return self.create_folder(self.data_folder_path)

    def init_flake_file(self):
        return self.make_file(self.flake_path)

    def init_unit_file(self):
        return self.make_file(self.unit_path)

    def create_folder(self, path):
        if exists(path) == False:
            makedirs(path)

        return path 

    def include_path(self, name: str):
        return join(self.root, INCLUDES_FOLDER, name)

    def create_includes(self, name: str):
        path = self.create_folder(self.include_path(name))
        self.create_folder(path)

    def make_file(self, path, content = ''):
        dir = dirname(path)

        if exists(dir) == False:
            makedirs(dir)

        with open(path, 'w') as f:
            f.write(content)

        return path 

