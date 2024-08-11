from ss.configure.schema import * 
from .renderer import Renderer
from typing import List, Dict

class NixTemplate:
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.renderer = Renderer(blueprint=blueprint)

    def render(self) -> str:
        return f"""
        {{ pkgs ? import <nixpkgs> {{}} }}:
        let
        {LINE_BREAK.join(self._nix_icludes_value())}
        name = "{self.blueprint.name}";
        version = "{self.blueprint.version}";
        units = pkgs.callPackage ./units.nix {{ inherit name version { ' '.join(self._nix_includes_names()) }; }};
        in

        {  self.render_mkshell() if self.blueprint.is_root_blueprint else self.render_package() }
        
        """

    def render_package(self):
        return f"units // {{ inherit name version { SPACE.join(self._nix_includes_names())}; }} // units.all_attr"

    def render_mkshell(self):
        return f"""
        pkgs.mkShell {{
            name = name;
            version = version;
            buildInputs = [
                units.all
            ];

            shellHook = ''
                echo "Welcome to ${{name}} shell"
                ${{units.scripts}}
            '';
        }}
        """

    def _nix_icludes_value(self) -> List[str]:
        return list(self._nix_includes().values())

    def _nix_includes_names(self) -> List[str]:
        return list(self._nix_includes().keys())

    def _nix_includes(self) -> Dict[str, str]:
        return { item[0]:item[1] for item in self.renderer.includes if item[1] is not None }

