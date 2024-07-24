from .template import Template

class NixGenerator(Template):
    def __init__(self, blueprint):
        super().__init__(blueprint)

    def render(self) -> str:
        return f"""
        {{ pkgs ? import <nixpkgs> {{}} }}:
        let
        {super().LINE_BREAK.join([ item[1] for item in self.includes if item[1] is not None])}
        name = "{self.blueprint.name}";
        version = "{self.blueprint.version}";
        units = pkgs.callPackage ./unit.nix {{ inherit { ' '.join([item[0] for item in self.includes if item[1] is not None]) }; }};
        in
        pkgs.mkShell {{
            name = name;
            version = version;
            buildInputs = [
                units
            ];

            shellHook = ''
                echo "Welcome to ${{name}} shell"
                ${{units.scripts}}
            '';
        }}
        """

