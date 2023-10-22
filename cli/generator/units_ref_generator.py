from file_generator import FileGenerator
from configure.configure import Configure
from functools import reduce

class UnitsRefGenerator(FileGenerator):
    def __init__(self, configure: Configure):
        self.configure = configure

    def generate(self):
        return self._render_units_ref()

    def _render_units_ref(self) -> str:
        all_units = reduce(lambda last, next: f'{last} {next}', map(lambda unit: unit.name, self.configure.units))
        return f'[ {all_units} ]'
