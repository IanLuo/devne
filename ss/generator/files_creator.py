from .units_template import UnitsTemplate
from .ss_nix_template import SSNixTemplate
from ..configure.blueprint import Blueprint
from ..folder import Folder
from os.path import join
from .service_template import ServiceTemplate
import os


class FilesCreator:
    def __init__(self, blueprint: Blueprint, root: str):
        self.blueprint = blueprint
        self.folder = Folder(join(root))

    def create_files(self):
        self.blueprint.resovle_all_includes(self.blueprint.includes)
        for name, include in self.blueprint.includes.items():
            blueprint = include.get("blueprint")
            if blueprint is not None:
                blueprint.resovle_all_includes(blueprint.includes)
                self.create(
                    blueprint=blueprint,
                    root=Folder(path=blueprint.gen_folder.path).include_path(name),
                )

        self.create(root=self.folder.path, blueprint=self.blueprint)
        self.copy_resource(blueprint=self.blueprint)

    def copy_resource(self, blueprint: Blueprint):
        folder_path = join(os.path.dirname(__file__), "nix")

        if not os.path.exists(folder_path):
            raise Exception(f"files not found in {folder_path}")

        import shutil

        shutil.copytree(folder_path, self.folder.lib_folder, dirs_exist_ok=True)

    def create(self, root: str, blueprint: Blueprint) -> bool:
        folder = Folder(root)
        units_template = UnitsTemplate(blueprint)
        ss_template = SSNixTemplate(blueprint)

        # create ss.nix
        self._write_to_file(
            ss_template.render(),
            folder.init_ss_file(),
        )

        # create unit.nix
        self._write_to_file(
            units_template.render(),
            folder.init_unit_file(),
        )

        return True

    def generate_services(self, profile: dict, blueprint: Blueprint) -> bool:
        content = ServiceTemplate(blueprint, profile).render()

        self._write_to_file(content, self.folder.init_services_file())

        return True

    def _write_to_file(self, content, path):
        with open(path, "w") as f:
            f.write(content)
