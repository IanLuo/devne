from .parser import parse 
from .unit import Unit
from typing import Optional
from os.path import dirname, exists
from ..folder import Folder
from jsonpath_ng import parser
from typing import TypeVar
from ..user_interactive.user_input_wizard import UserInputWizard, InputItem 

T = TypeVar('T')

class Configure:
    def __init__(self, config_path):
        self.root = dirname(config_path)

        if not exists(config_path):
            raise Exception(f"config file not existed: {config_path}")

        with open(config_path, 'r') as f:
            yaml = f.read()
            self._config = parse(yaml)

    @staticmethod
    def init_empty_config(config_path: str):
        config_wizard = UserInputWizard([
            InputItem('name', False),
            InputItem('version', True),
            InputItem('language', False),
            InputItem('version of language', False),
        ])

        config = config_wizard.run()
        print(config)
        return

        folder = Folder(dirname(config_path))
        if not exists(folder.config_path):
            folder.make_empty_file(folder.init_config_file())
        else:
            print('config file already exists')

    def _find_value(self, key_path: str, default: T) -> T: 
        jsonpath_expr = parser.parse(key_path)
        result = jsonpath_expr.find(self._config)
        if len(result) > 0:
            value = result[0].value

            if type(value) == type(default):
                return value 

        return default

    @property
    def sdk_language(self) -> str:
         return self._find_value("$.sdk.language", '')

    @property
    def sdk_version(self) -> str:
        return self._find_value("$.sdk.version", '')

    @property
    def sdk_packages_default(self) -> list[str]:
        return self._find_value("$.sdk.packages.default", [])

    @property
    def sdk_packages_dev(self) -> list[str]:
        return self._find_value("$.sdk.packages.development", [])

    @property
    def dependencies_default(self) -> list[str]:
        return self._find_value("$.dependencies.default",[]) 

    @property
    def dependencies_dev(self) -> list[str]:
        return self._find_value("$.dependencies.development", [])

    @property
    def units(self) -> list[Unit]:
        def _get_unit(unit) -> Optional[Unit]:
            if type(unit) is str:
                return Unit(name=unit)
            elif type(unit) is dict:
                return Unit(json=unit)
            else:
                return None

        units = self._find_value('$.units', [])

        return [ value for value in map(lambda unit: _get_unit(unit), units) if value is not None ]

    @property
    def ref(self) -> str:
        return self._find_value("$.pkgsrev", '')

    @property
    def name(self) -> str:
        return self._find_value("$.name", '')

    @property
    def version(self) -> str:
        return self._find_value("$.version", '')

    @property
    def description(self) -> str:
        return self._find_value("$.description", '')
