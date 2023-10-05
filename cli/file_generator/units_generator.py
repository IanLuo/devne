from typing import List
from .unit import Unit

TEMPLATE_FILE = 'units.nix.template'

class UnitsGenerator:
    def __init__(self, units: List[Unit]):
        self.units = units

    def read_template(self, template_file: str):
        self.template = open(template_file, 'r').read() 

    def generate(self):
        pass
