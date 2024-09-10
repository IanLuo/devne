from .nix_template import NixTemplate
from .units_template import UnitsTemplate
from ..configure.blueprint import Blueprint
from ..folder import Folder
from os.path import join
import os

class FilesCreator:
    def __init__(self, blueprint: Blueprint, root: str):
        self.blueprint = blueprint
        self.folder = Folder(join(root, '.ss'))

    def create_all(self):
        self.blueprint.resovle_all_includes(self.blueprint.includes)
        for (name, include) in self.blueprint.includes.items():
            blueprint = include.get('blueprint')
            if blueprint is not None:
                blueprint.resovle_all_includes(blueprint.includes)
                self.create(blueprint= blueprint, root=self.folder.include_path(name))

        self.create(root=self.folder.path, blueprint=self.blueprint)
        self.copy_resource(blueprint=self.blueprint)

    def copy_resource(self, blueprint: Blueprint) -> bool:
        folder_path = join(os.path.dirname(__file__), 'nix')

        if not os.path.exists(folder_path):
            raise Exception(f'files not found in {folder_path}')

        import shutil
        nix_folder_path = os.path.join(self.blueprint.gen_folder.path, 'nix')
        shutil.copytree(folder_path, nix_folder_path, dirs_exist_ok=True)

    def create(self, root: str, blueprint: Blueprint) -> bool:
        folder = Folder(root)
        flake_template = NixTemplate(blueprint)
        units_template = UnitsTemplate(blueprint)

        # creat flake.nix
        self._write_to_file(flake_template.render(), folder.init_flake_file())

        # create unit.nix
        self._write_to_file(units_template.render(), folder.init_unit_file())

        return True

    def _write_to_file(self, content, path):
        with open(path, "w") as f:
            f.write(content)
