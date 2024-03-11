from .template import Template
from ..configure.configure import Configure
from dataclasses import dataclass
from .str_render import StrRender


@dataclass
class FlakeTemplate(Template):
    configure: Configure

    def render(self) -> str:
        return StrRender(
            f"""
      {{
        description = "{self.configure.metadata.description}";

        inputs.nixpkgs = {{
          url = "github:NixOS/nixpkgs/{self.configure.sources['pkgs'].value}";
        }};

        inputs.flake-utils.url = "github:numtide/flake-utils";

        inputs.sstemplate.url = "github:ianluo/ss-templates";
        inputs.sstemplate.inputs.nixpkgs.follows = "nixpkgs";

        outputs = {{ self, nixpkgs, flake-utils, sstemplate }}:
          flake-utils.lib.eachDefaultSystem (system:
            let
              pkgs = import nixpkgs {{ inherit system; }};

              version = "{self.configure.metadata.version}";
              name = "{self.configure.metadata.name}";

              units = pkgs.callPackage ./units.nix {{ inherit sstemplate name version system; }};
            in
            {{
              devShells = with pkgs; {{
                default = mkShell {{
                  name = name;
                  version = version;
                  buildInputs = (map (x: x.value) units.all);

                  shellHook = ''
                    ${{units.scripts}}
                  '';
                }};
              }};

              packages = units.packages;
            }});
      }}
      """
        ).render
