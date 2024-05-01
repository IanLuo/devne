from .template import Template
from dataclasses import dataclass
from ..configure.blueprint import *


@dataclass
class FlakeTemplate(Template):
    blueprint: Blueprint

    def _render_inputs(self, item: tuple):
        name = item[0]
        content = item[1]
        if name in super().SYS_SOURCE_NAME:
            return ""
        return f"""
            {name} = {{
               url = "{content['url']}";
            }};
        """

    def render(self) -> str:
        filter_sys_sources = super().filter_sys_sources

        return f"""
      {{
        description = "{self.blueprint.description}";

        inputs = {{
            flake-utils.url = "github:numtide/flake-utils";
        {super().LINE_BREAK.join(map(self._render_inputs, self.blueprint.includes.items()))}
        }};

        outputs = {{ self, flake-utils, flake-parts, {','.join([key for key in self.blueprint.includes.keys()])}  }}:
          flake-utils.lib.eachDefaultSystem (system:
            let
              pkgs = nixpkgs.legacyPackages.${{system}};

              version = "{self.blueprint.version}";
              name = "{self.blueprint.name}";

              units = pkgs.callPackage ./units.nix {{ inherit name version ss; nixpkgs = pkgs; }};
            in
            {{
              devShells = with pkgs; {{
                default = mkShell {{
                  name = name;
                  version = version;
                  packages = units.dependencies;

                  shellHook = ''
                    ${{units.scripts}}
                  '';
                }};
              }};
            }});
      }}
      """
