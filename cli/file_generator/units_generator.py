from typing import List
from configure.unit import Unit
from configure.configure import Configure
from flake_generator import FileGenerator

TEMPLATE_FILE = 'units.nix.template'

class UnitsGenerator(FileGenerator):
    def __init__(self, configure: Configure):
        self.configure = configure

    def read_template(self, template_file: str):
        self.template = open(template_file, 'r').read() 

    def generate(self):
        # TODO:
        pass

    def fill_in_template(self, template: str, units: List[Unit]):
        # TODO:
        pass
