from typing import Any
from ss.configure.blueprint import Blueprint
from os.path import exists
from ss.generator.functions.function_factory import find_function
from ss.configure.schema import *

class Renderer:
    def __init__(self, blueprint: Blueprint):
        self.blueprint = blueprint
        self.includes = [ self.resolve_import(name=item[0], item=item[1]) for item in self.blueprint.includes.items()]


    def resolve_import(self, name: str, item: dict):
        local_path = item.get("local_path")
        gen_root = item.get("gen_root")
        ss_nix = f'{gen_root}/ss.nix'
        ss_yaml = f'{local_path}/ss.yaml'
        default_nix = f'{local_path}/default.nix'
        flake_nix = f'{local_path}/flake.nix'
        shell_nix = f'{local_path}/shell.nix'

        # if exists(ss_yaml):
        #     return name, f'{name} = pkgs.callPackage {ss_nix} {{}};'

        if exists(default_nix):
            return name, f'{name} = pkgs.callPackage {default_nix} {{}};'

        elif exists(flake_nix):
            return name, f'{name} = pkgs.importFlake {flake_nix} {{}};'

        elif exists(shell_nix):
            return f'{name} = pkgs.callPackage {shell_nix} {{}};'
        else: 
            return name, None 


    def _is_path(self, value: str) -> bool:
        return value.startswith("./") or value.startswith("../")

    def _is_multiple_lines(self, value: str) -> bool:
        return "\n" in value

    def merge_all_fields(self, unit: dict, blueprint: Blueprint) -> dict:
        source = unit.get(K_SOURCE, '')
        resolvable_includes = [ item for item in blueprint.includes.keys() if blueprint.includes[item].get('blueprint') is not None ]

        for resolvable_include in resolvable_includes:
            include = blueprint.includes[resolvable_include]
            source_comp = source.split('.')
            if len(source_comp) > 1:
                include_unit = include.get('blueprint').units.get(source_comp[1])
                if include_unit is not None:
                    # because 'source' is worked like 'father', so the child's source should be overrided by the father, other fields will use child's 
                    # None fields should be removed from child
                    unit = { key: value for key, value in unit.items() if value is not None and key != K_SOURCE }
                    unit = { **include_unit, **unit  }
                if len(source_comp) > 2:
                    unit = self.merge_all_fields(unit, blueprint.includes[resolvable_include].get('blueprint'))

        return unit


    def render_unit(self, unit: dict) -> str:
        keys_to_remove_as_parms = [K_SOURCE, K_INSTANTIATE, K_ACTIONS, K_LISTNER]

        # resolve all fields from includes
        unit = self.merge_all_fields(unit=unit, blueprint=self.blueprint)

        params = { k: v for k, v in unit.items() if k not in keys_to_remove_as_parms }

        def render_map(name:str, data: dict) -> str:
            function = find_function(name=name, value=data, params=params, blueprint=self.blueprint)
            if function is not None:
                return function.render()
            else:
                return f"""
                    {{
                        { LINE_BREAK.join([f'{key} = {render_value(key, value)};' for key, value in data.items() ]) }
                    }}
                """

        def render_value(name: str, value: Any) -> str:
            if value == None:
                return "null"
            elif isinstance(value, list):
                return f"""[{LINE_BREAK.join(map(lambda x: f'{render_value(name, x)}', value))}]"""
            elif isinstance(value, dict):
                return render_map(name=name, data=value)
            elif isinstance(value, bool):
                return "true" if value else "false"
            elif isinstance(value, str) and self._is_path(value):
                return value
            elif isinstance(value, str) and self._is_multiple_lines(value):
                q = "''"
                return f'''
                    {q}{value}{q}
                ''' 
            elif name == K_SOURCE: # in source, the text by default is supposed to be nix code, don't add quote
                return f'{str(value)}'
            else:
                return f'"{str(value)}"'

        return LINE_BREAK.join([f'{key}={render_value(key, value)};' for key, value in unit.items()]) 
