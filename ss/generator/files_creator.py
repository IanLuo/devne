from .nix_generator import NixGenerator 
from .units_template import UnitsTemplate
from ..configure.blueprint import Blueprint
from ..folder import Folder


class FilesCreator:
    def __init__(self, blueprint: Blueprint, root: str):
        self.blueprint = blueprint
        self.root = root

    def create_all(self):
        self.blueprint.resovle_all_includes(self.blueprint.includes)
        for (name, include) in self.blueprint.includes.items():
            blueprint = include.get('blueprint')
            if blueprint is not None:
                blueprint.resovle_all_includes(blueprint.includes)
                self.create(blueprint= blueprint, root=Folder(self.root).include_path(name))

        self.create(root=self.root, blueprint=self.blueprint)


    def create(self, root: str, blueprint: Blueprint) -> bool:
        folder = Folder(root)
        flake_template = NixGenerator(blueprint)
        units_template = UnitsTemplate(blueprint)

        # creat flake.nix
        self._write_to_file(flake_template.render(), folder.init_flake_file())

        # create unit.nix
        self._write_to_file(units_template.render(), folder.init_unit_file())

        return True

    def _write_to_file(self, content, path):
        with open(path, "w") as f:
            f.write(content)
