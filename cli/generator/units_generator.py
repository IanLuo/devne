from ..configure.unit import Unit
from ..configure.configure import Configure
from .file_generator import FileGenerator
from functools import reduce
import os

_TEMPLATE_FILE = 'templates/units.nix.template'
_MARK_UNITS = '#UNITS#'
_MARK_UNITS_REF = '#UNITS_REF#'

class UnitsGenerator(FileGenerator):
    def __init__(self, configure: Configure):
        self.configure = configure

    def generate(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_directory, _TEMPLATE_FILE)
        with open(path, 'r') as f:
            template = f.read()
            result = template.replace(_MARK_UNITS, self._read_units(self.configure))
            return result.replace(_MARK_UNITS_REF, self._render_units_ref(self.configure))
            

    def _read_units(self, configure: Configure) -> str:
        return reduce(lambda last, next: f'{last}\n{next}', map(self._render_unit, configure.units))

    def _render_unit(self, unit: Unit) -> str:
        return f'''
            {unit.name} = {unit.name} {{
                {reduce(lambda last, next: f'{last}{next}', (f'{key}={value};' for key, value in unit.attrs) )}
            }} 
        '''

    def _render_units_ref(self, configure: Configure) -> str:
        all_units = reduce(lambda last, next: f'{last} {next}', map(lambda unit: unit.name, configure.units))
        return f'[ {all_units} ]'
        

