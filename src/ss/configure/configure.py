from dataclasses import dataclass
from .parser import parse 
from .unit import Unit
from os.path import dirname, exists
from ..folder import Folder
from jsonpath_ng import parser
from ..user_interactive.user_input_wizard import UserInputWizard, InputItem 
from ..resources.remote.global_configure import GlobalConfigure 
from .git_repo import GitRepo
from typing import Optional
import re

@dataclass
class Configure:
    name: str
    version: str
    description: str
    tools: list[str]
    units: list[Unit]
    nixpkgsrev: str
    root: str

    def __init__(self, config_path):
        self.root = dirname(config_path)

        if not exists(config_path):
            raise Exception(f"config file not existed: {config_path}")

        with open(config_path, 'r') as f:
            yaml = f.read()
            resolved_yaml = self._resolve_vars(yaml, parse(yaml))
            self._config = parse(resolved_yaml)

        self._read_config()

    def _read_config(self):
        # read metadata
        self.name = self._find_value('$.metadata.name', self._config) or ''
        self.version = self._find_value('$.metadata.version', self._config) or ''
        self.description = self._find_value('$.metadata.description', self._config) or ''
        # read units 
        self.units = self._find_units(self._find_value('$.units', self._config) or []) or []
        # read tools
        self.tools = self._find_value('$.tools', self._config) or []
        # read nixpkgsrev
        self.nixpkgsrev = self._find_value('$.nixpkgsrev', self._config) or ''

    def _resolve_vars(self, config: str, parsed_config: dict):
        pattern = r'\$\{(.*)\}'
        first_match = re.search(pattern, config)

        if first_match is None:
            return config
        else:
            var_name = first_match.group(1) or ''
            var_value = self._find_value(f'$.{var_name}', parsed_config) or ''
            new_config = config.replace(f'${{{var_name}}}', var_value)
            return self._resolve_vars(new_config, parsed_config)


    def _find_value(self, key_path: str, config: dict): 
        jsonpath_expr = parser.parse(key_path)
        result = jsonpath_expr.find(config)

        if len(result) > 0:
            return result[0].value
        else:
            return None

    def _find_units(self, units: list) -> list[Unit]:
        units_in_json = [ Unit(json=unit) for unit in units if isinstance(unit, dict) ]
        units_in_str = [ Unit(name=unit) for unit in units if isinstance(unit, str) ]

        def flatten_list(nested_list):
            return [item for sublist in nested_list for item in (flatten_list(sublist) if isinstance(sublist, list) else [sublist])]

        nested_units = flatten_list([ [ value for _, value in unit.attrs.items() if isinstance(value, Unit)] for unit in units_in_json ])

        return units_in_json + units_in_str + nested_units

    @staticmethod
    def init_default_config(config_path: str):
        folder = Folder(dirname(config_path))

        if not exists(folder.config_path):
            config_wizard = UserInputWizard([
                InputItem(False, 'name'),
                InputItem(False, 'version'),
                InputItem(False, 'language'),
                InputItem(False, 'version of language' ),
                InputItem(False, 'description'),
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
        else:
            raise Exception('config file already exists')
