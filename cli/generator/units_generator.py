from ..configure.unit import Unit
from ..configure.configure import Configure
from .file_generator import FileGenerator
from functools import reduce

class UnitsGenerator(FileGenerator):
    def __init__(self, configure: Configure):
        self.configure = configure

    def generate(self):
        return self._read_units()

    def _read_units(self) -> str:
        return reduce(lambda result, next: f'{result}\n{next}', map(self._render_unit, self.configure.units))

    def _render_unit(self, unit: Unit) -> str:
        kvs = [f'{key} = "{value}"' for key, value in unit.attrs.items()]
        make_units = lambda kvs: reduce(lambda result, next: f'{result}\n{next}', kvs)

        return f'''
            {unit.name} = {{
                {make_units(kvs)}
            }};
        '''
