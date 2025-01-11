CONFIG_FILE = "ss.yaml"
LOCK_FILE = "ss.lock"
SS_FILE = "ss.nix"
UNIT_FILE = "units.nix"
SERVICES_FILE = "services.yaml"
DATA_FOLDER = ".ss"
INCLUDES_FOLDER = "includes"
LIB_FOLDER = "nix"

from os.path import exists, dirname, join, abspath
from os import makedirs
import os


class Folder:
    def __init__(self, path: str):
        self.path = path

    @staticmethod
    def at_current_location(path: str):
        return join(dirname(abspath(__file__)), path)

    def ss_path(self, is_root: bool):
        if is_root:
            return join(self.path, DATA_FOLDER, SS_FILE)
        else:
            return join(self.path, SS_FILE)

    def unit_path(self, is_root: bool):
        if is_root:
            return join(self.path, DATA_FOLDER, UNIT_FILE)
        else:
            return join(self.path, UNIT_FILE)

    @property
    def data_folder_path(self):
        return join(self.path, DATA_FOLDER)

    @property
    def config_path(self):
        return join(self.path, CONFIG_FILE)

    @property
    def lock_path(self):
        return join(self.path, LOCK_FILE)

    def include_path(self, name: str):
        return join(self.path, INCLUDES_FOLDER, name)

    @property
    def lib_folder(self):
        return join(self.path, DATA_FOLDER, LIB_FOLDER)

    @property
    def services_path(self):
        return join(self.path, DATA_FOLDER, SERVICES_FILE)

    def init_data_path(self) -> str:
        return self.create_folder(self.data_folder_path)

    def init_ss_file(self, is_root: bool):
        return self.make_file(self.ss_path(is_root=is_root))

    def init_unit_file(self, is_root: bool):
        return self.make_file(self.unit_path(is_root=is_root))

    def init_services_file(self):
        return self.make_file(self.services_path)

    def create_folder(self, path):
        if exists(path) == False:
            makedirs(path)

        return path

    def all_files(self, ext):
        matching_files = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith(ext):
                    matching_files.append(os.path.join(root, file))
        return matching_files

    def make_file(self, path, content=""):
        dir = dirname(path)

        if exists(dir) == False:
            makedirs(dir)

        with open(path, "w") as f:
            f.write(content)

        return path
