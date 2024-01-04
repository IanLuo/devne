from ..configure.unit import Unit
from ..configure.configure import Configure
from .interface.content_generator import ContentGenerator
from .interface.file_exporter import FileExporter
import os

_UNITS_TEMPLATE_FILE = './templates/units.nix.template'

_MARK_UNITS = '#UNITS#'
_MARK_UNITS_REF = '#UNITS_REF#'

class UnitsGenerator(ContentGenerator, FileExporter):
    def __init__(self, configure: Configure):
        self.configure = configure

    def generate(self) -> dict:
        return { k: v for k, v in {
            _MARK_UNITS: self._render_all_units(),
            _MARK_UNITS_REF: self._render_units_ref(),
        }.items() if v is not None }

    def export(self) -> str:
        return self._generate_units_file_content()

    def _render_all_units(self) -> str:
        return '\n'.join(map(self._render_unit, self.configure.units or []))

    def _render_unit(self, unit: Unit) -> str:
        result = '' 
        _render_unit_name = lambda unit: unit.name.replace('.', '_')
        def _dig_value(value):
            def _is_path(value):
                if not isinstance(value, str):
                    return False
                elif value.startswith('./') or value.startswith('../'):
                    return True

                return False

            def _is_unit(value):
                return isinstance(value, Unit)

            def _is_unit_ref(value):
                return isinstance(value, str) and value.startswith('$')

            if _is_unit(value):
                return _render_unit_name(value)
            elif _is_path(value):
                return value;
            elif _is_unit_ref(value):
                unit_ref_name = value.replace('$', '').replace('.', '_')
                if unit_ref_name.find('>') != -1:
                    return unit_ref_name.replace('>', '.')
                else:
                    return f'if {unit_ref_name}.value == null then {unit_ref_name} else {unit_ref_name}.value'
            elif isinstance(value, str):
                return f'"{value}"'
            elif isinstance(value, list):
                inner =  " ".join([f'"{v}"' for v in value])
                return f'[ {inner} ]'
            elif value == None:
                return "null"
            else:
                return value

        # put 4 spaces before each line
        kvs = [f'    {key} = {_dig_value(value)};' for key, value in unit.attrs.items()]
        make_units = lambda kvs: '\n'.join(kvs)

        result = f'''
{result}
  {_render_unit_name(unit)} = {unit.name} {{
{make_units(kvs)}
  }};
        '''

        return result

    def _render_units_ref(self) -> str:
        all_units = ' '.join(map(lambda unit: unit.name.replace(".", "_"), self.configure.units or []))

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
