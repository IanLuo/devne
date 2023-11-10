from .parser import parse 
from .unit import Unit
from typing import Optional
from os.path import dirname, exists
from ..folder import Folder
from jsonpath_ng import parser
from typing import TypeVar
from ..user_interactive.user_input_wizard import UserInputWizard, InputItem 
from ..resources.remote.global_configure import GlobalConfigure 

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
    def init_default_config(config_path: str):
        folder = Folder(dirname(config_path))

        if not exists(folder.config_path):
            config_wizard = UserInputWizard([
                InputItem('name', False),
                InputItem('version', False),
                InputItem('language', False),
                InputItem('version of language', False),
                InputItem('description', False),
            ])

            config = config_wizard.run()
            name = config['name']
            version = config['version']
            language = config['language']
            version_of_language = config['version of language']
            description = config['description']
            nixpkgs_rev = GlobalConfigure.fetch_nixpkgs_rev()

            current_directory = dirname(__file__)
            path = f'{current_directory}/ss.yaml.template'
            with open(path, 'r') as f:
                content = f.read()
                content = content.replace('#NAME#', name)
                content = content.replace('#DESCRIPTION#', description)
                content = content.replace('#VERSION#', version)
                content = content.replace('#SDK_LANGUAGE#', language)
                content = content.replace('#SDK_VERSION#', version_of_language)
                content = content.replace('#NIXPKGSREV#', nixpkgs_rev)
                folder.make_file(folder.config_path, content)

            folder.make_file(folder.init_config_file(), content)
        else:
            raise Exception('config file already exists')

    def _find_value(self, key_path: str): 
        jsonpath_expr = parser.parse(key_path)
        result = jsonpath_expr.find(self._config)
        return str(result[0].value)

    @property
    def sdk_language(self) -> str:
         return self._find_value("$.sdk.language")

    @property
    def sdk_version(self) -> str:
        return self._find_value("$.sdk.version")

    @property
    def sdk_packages_default(self) -> list[str]:
        return self._find_value("$.sdk.packages.default")

    @property
    def sdk_packages_dev(self) -> list[str]:
        return self._find_value("$.sdk.packages.development")

    @property
    def tools(self) -> list[str]:
        return self._find_value("$.tools") 

    @property
    def units(self) -> list[Unit]:
        def _get_unit(unit) -> Optional[Unit]:
            if type(unit) is str:
                return Unit(name=unit)
            elif type(unit) is dict:
                return Unit(json=unit)
            else:
                return None

        units = self._find_value('$.units')

        return [ value for value in map(lambda unit: _get_unit(unit), units) if value is not None ]

    @property
    def nixpkgsrev(self) -> str:
        return self._find_value("$.nixpkgsrev")

    @property
    def name(self) -> str:
        return self._find_value("$.name")

    @property
    def version(self) -> str:
        return self._find_value("$.version")

    @property
    def description(self) -> str:
        return self._find_value("$.description")
