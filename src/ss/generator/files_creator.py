from .flake_template import FlakeTemplate
from .units_template import UnitsTemplate
from ..configure.blueprint import Blueprint
from ..folder import Folder
from os.path import exists


class FilesCreator:
    def __init__(self, blueprint: Blueprint, root: str):
        self.folder = Folder(root)
        self.flake_template = FlakeTemplate(blueprint)
        self.units_template = UnitsTemplate(blueprint)

    def create(self) -> bool:
        # creat flake.nix
        self._write_to_file(self.flake_template.render(), self.folder.init_flake_file())

        # create unit.nix
        self._write_to_file(self.units_template.render(), self.folder.init_unit_file())

        return True

    def _write_to_file(self, content, path):
        with open(path, "w") as f:
            f.write(content)
