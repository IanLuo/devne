CONFIG_FILE = "ss.yaml"
LOCK_FILE = "ss.lock"
SS_FILE = "ss.nix"
UNIT_FILE = "units.nix"
SERVICES_FILE = "services.yaml"
GEN_FOLDER = ".ss"
INCLUDES_FOLDER = "includes"
LIB_FOLDER = "nix"
LOG_FOLDER = "logs"
DATA_FOLDER = "data"

from os.path import exists, dirname, join, abspath
from os import makedirs
import os


class Global:
    _instance = None
    _project_root = None

    @property
    def project_root(self):
        if self._project_root is None:
            raise ValueError("Project root not set")
        return self._project_root

    @project_root.setter
    def project_root(self, value):
        self._project_root = value

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Global, cls).__new__(cls)
            cls._instance._data = {}
        return cls._instance


class Folder:
    def __init__(self, path: str):
        self.path = path

    @property
    def is_root(self):
        return self.path == Global().project_root

    @staticmethod
    def set_root(root):
        Global().project_root = root

    @staticmethod
    def at_current_location(path: str):
        return join(dirname(abspath(__file__)), path)

    def ss_path(self):
        if self.is_root:
            return join(self.path, GEN_FOLDER, SS_FILE)
        else:
            return join(self.path, SS_FILE)

    def unit_path(self):
        if self.is_root:
            return join(self.path, GEN_FOLDER, UNIT_FILE)
        else:
            return join(self.path, UNIT_FILE)

    @property
    def gen_folder_path(self):
        return join(self.path, GEN_FOLDER)

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
        return join(self.path, GEN_FOLDER, LIB_FOLDER)

    @property
    def services_path(self):
        return join(self.path, GEN_FOLDER, SERVICES_FILE)

    def init_data_path(self) -> str:
        return self.create_folder(self.gen_folder_path)

    def init_ss_file(self):
        return self.make_file(self.ss_path())

    def init_unit_file(self):
        return self.make_file(self.unit_path())

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
