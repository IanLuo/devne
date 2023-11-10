from ..configure.unit import Unit
from ..configure.configure import Configure
from .interface.content_generator import ContentGenerator
from .interface.file_exporter import FileExporter
from functools import reduce
from .sdk_generator import SdkGenerator
import os

_UNITS_TEMPLATE_FILE = './templates/units.nix.template'

_MARK_UNITS = '#UNITS#'
_MARK_SDK = '#SDK#'
_MARK_UNITS_REF = '#UNITS_REF#'

class UnitsGenerator(ContentGenerator, FileExporter):
    def __init__(self, configure: Configure):
        self.configure = configure
        self.sdk_generator = SdkGenerator(configure) 

    def generate(self) -> dict:
        return { k: v for k, v in {
            _MARK_UNITS: self._render_all_units(),
            _MARK_UNITS_REF: self._render_units_ref(),
            _MARK_SDK: self._render_sdk()
        }.items() if v is not None }

    def export(self) -> str:
        return self._generate_units_file_content()

    def _render_all_units(self) -> str:
        return '\n'.join(map(self._render_unit, self.configure.units))

    def _render_unit(self, unit: Unit) -> str:
        kvs = [f'{key} = "{value}";' for key, value in unit.attrs.items()]
        make_units = lambda kvs: '\n'.join(kvs)

        return f'''
            {unit.name} = {{
                {make_units(kvs)}
            }};
        '''

    def _render_sdk(self) -> str:
        if self.configure.sdk_language == 'python':
            return self.sdk_generator.export_python()
        else: 
            return ''

    def _render_units_ref(self) -> str:
        all_units = ' '.join(map(lambda unit: unit.name, self.configure.units))

        if len(all_units) == 0:
            return '[]' 

        return f'[ {all_units} ]'

    def _generate_units_file_content(self) -> str:
        '''Generate units.nix file, units and units ref are all in this file'''

        current_directory = os.path.dirname(os.path.abspath(__file__))
        path = os.path.join(current_directory, _UNITS_TEMPLATE_FILE)

        with open(path, 'r') as f:
            template = f.read()

            for key, value in self.generate().items():
                template = template.replace(key, value)

            return template
