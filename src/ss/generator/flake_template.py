from .template import Template
from ..configure.configure import Configure, Source
from dataclasses import dataclass


@dataclass
class FlakeTemplate(Template):
    configure: Configure

    def _replace_source_name_if_needed(self, source_name) -> str:
        map_source_name = {
            'pkgs': 'nixpkgs'
        }

        return map_source_name.get(source_name, source_name)

    def _render_inputs(self, source: Source):
        pre_defined = {
            'sstemplate': 'github:ianluo/ss-templates',
            'pkgs': 'github:ianluo/ss-templates'
            }

        prefix = lambda source: pre_defined.get(source.name, None) or ''

        return f'''
            {self._replace_source_name_if_needed(source.name)} = {{
               url = "{prefix(source)}{source.url}";
            }};
        '''

    def render(self) -> str:
        return f"""
      {{
        description = "{self.configure.metadata.description}";

        inputs = {{
        flake-utils.url = "github:numtide/flake-utils";
        {super().LINE_BREAK.join(map(self._render_inputs, self.configure.sources.values()))}
        }};

        outputs = {{ self, flake-utils, {','.join( self._replace_source_name_if_needed(key) for key in self.configure.sources.keys())}  }}:
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
