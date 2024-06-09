from .template import Template
from dataclasses import dataclass
from ..configure.blueprint import *
from urllib.parse import urlparse, urlunparse


@dataclass
class FlakeTemplate(Template):
    blueprint: Blueprint

    def _render_inputs(self, item: tuple):
        name = item[0]
        content = item[1]

        url = content['url']
        scheme = self.get_scheme(url);
        url_without_scheme = self.remove_scheme(url);
        is_flake = 'true' if content.get('flake', True) else 'false'

        if scheme == 'path':
            return f"""
            {name} = {{
               url = "{url}";
               flake = {is_flake};
            }};
        """
        else:
            return f"""
                {name} = {{
                   url = "git+https:{url_without_scheme}?rev={content['rev']}";
                   flake = {is_flake};
                }};
            """

    def get_scheme(self, url):
        # Parse the URL into components
        parsed_url = urlparse(url)
        
        # Return the scheme component
        return parsed_url.scheme

    def remove_scheme(self, url):
        # Parse the URL into components
        parsed_url = urlparse(url)
        
        # Reconstruct the URL without the scheme
        url_without_scheme = urlunparse(('', parsed_url.netloc, parsed_url.path, parsed_url.params, parsed_url.query, parsed_url.fragment))
        
        return url_without_scheme

    def render(self) -> str:
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
              libs = units;
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
