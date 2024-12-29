from ss.configure.schema_gen import schema, LINE_BREAK, SPACE
from .renderer import Renderer
from typing import List, Dict


class SSNixTemplate:
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.renderer = Renderer()

    def render(self) -> str:
        return f"""
        {{ pkgs ? import <nixpkgs> {{}} }}:
        let
        {LINE_BREAK.join(self._nix_icludes_value())}
        sslib = pkgs.callPackage {self.blueprint.gen_folder.path}/nix/sslib.nix {{}};
        name = "{self.blueprint.name}";
        version = "{self.blueprint.version}";
        units = pkgs.callPackage ./units.nix {{ inherit pkgs name version sslib { ' '.join(self._nix_includes_names()) }; }};
        in

        {  self.render_mkshell() if self.blueprint.is_root_blueprint else self.render_package() }

        """

    def render_package(self):
        return f"{{ isSS = true; }} // units // {{ inherit pkgs name version { SPACE.join(self._nix_includes_names())}; }} // units.allAttr"

    def render_mkshell(self):
        return f"""
        pkgs.mkShellNoCC {{
            name = name;
            version = version;
            buildInputs = [
                units.all
            ] ++ units.funcs;

            shellHook = ''
                ${{units.scripts}}
            '';
        }}
        """

    def _nix_icludes_value(self) -> List[str]:
        return list(self._nix_includes().values())

    def _nix_includes_names(self) -> List[str]:
        return list(self._nix_includes().keys())

    def _nix_includes(self) -> Dict[str, str]:
        return {
            item[0]: item[1]
            for item in self.renderer.resolve_all_includes(blueprint=self.blueprint)
            if item[1] is not None
        }
