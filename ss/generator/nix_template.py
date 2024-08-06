from ss.configure.schema import * 
from os.path import exists
from .renderer import Renderer

class NixTemplate:
    def __init__(self, blueprint):
        self.blueprint = blueprint
        self.renderer = Renderer(blueprint=blueprint)

    def render(self) -> str:
        return f"""
        {{ pkgs ? import <nixpkgs> {{}} }}:
        let
        {LINE_BREAK.join([ item[1] for item in self.renderer.includes if item[1] is not None])}
        name = "{self.blueprint.name}";
        version = "{self.blueprint.version}";
        units = pkgs.callPackage ./units.nix {{ inherit name version { ' '.join([item[0] for item in self.renderer.includes if item[1] is not None]) }; }};
        in

        {  self.render_mkshell() if self.blueprint.is_root_blueprint else self.render_package() }
        
        """

    def render_package(self):
        return f"units // {{ inherit name version; }} // units.all_attr"

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

