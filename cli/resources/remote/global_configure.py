import requests
import yaml
import os

class GlobalConfigure: 
    @staticmethod
    def fetch_nixpkgs_rev():
        current_directory = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_directory, 'remote.yaml')

        with open(path) as f:
            yaml_file = yaml.load(f, Loader=yaml.FullLoader)
            nix_pkgs_rev = yaml_file['source']

            if nix_pkgs_rev == None:
                raise Exception('nixpkgs revision not found')

        return requests.get(nix_pkgs_rev).text

