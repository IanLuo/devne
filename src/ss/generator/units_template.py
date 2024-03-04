from ..configure.configure import Configure
from .template import Template
from dataclasses import dataclass
from typing import List
from .str_render import StrRender
from ..configure.functions.git_repo import GitRepo


@dataclass
class UnitsTemplate(Template):
    configure: Configure

    def _render_map(self, data: dict) -> str:
        line_break = "\n"
        return f"""{{ {line_break.join([ f'{key} = {self._render_value(value)};' for key, value in data.items() ])} }}"""

    def _render_value(self, value) -> str:
        if isinstance(value, list):
            return f"""[{" ".join(map(lambda x: f'"{x}"', value))}];"""
        elif isinstance(value, dict):
            return self._render_map(value)
        elif isinstance(value, bool):
            return "true" if value else "false"
        elif isinstance(value, GitRepo):
            return StrRender(
                f"""
				TODO: render git repo
			"""
            ).render
        else:
            return f'"{value}"'

    def _render_from_pkgs(self, config: Configure) -> List[str]:
        units = [
            unit.definition
            for unit in config.all_unit_instances
            if unit.source.name == "pkgs"
        ]

        line_break = "\n"

        render_unit = lambda unit: StrRender(
            f"""
		# TODO: wrap every dev inside a unit
			pkgs.{unit.name}.overrideAttrs { self._render_map(unit.attrs) }
		"""
        ).render

        return map(render_unit, units)

    def _render_from_units_template(self, config: Configure) -> List[str]:
        units = [
            unit.definition
            for unit in config.all_unit_instances
            if unit.source.name == "units"
        ]

        line_break = "\n"

        render_unit = lambda unit: StrRender(
            f"""
				template.{unit.name.replace('_', '.')} { self._render_map(unit.attrs) }
				"""
        ).render

        return map(render_unit, units)

    def _render_from_customized(self, config: Configure) -> str:
        return ""

    def render(self) -> str:
        space = " "
        return StrRender(
            f"""
	{{ sstemplate, system, name, version, lib, pkgs }}:
		let
		template = import sstemplate {{ inherit system pkgs; }};

		all = lib.lists.filter (x: x.isUnit) (
			[
				{space.join(map(lambda x: f'({x})', self._render_from_pkgs(self.configure)))}
			]
			++
			[
				{space.join(map(lambda x: f'({x})', self._render_from_units_template(self.configure)))}
			]);

		startScript = ''
			export SS_PROJECT_BASE=$PWD
		'';
		in {{
		inherit all;
		scripts = builtins.concatStringsSep "\\n" ([ startScript ] ++ map (unit: unit.script) all);
		packages = lib.attrsets.genAttrs
					(map
						(x: x.value.pname)
						(lib.lists.filter (x: x.isPackage) all))

					(name:
						(lib.lists.findFirst (x: x.isPackage && x.value.pname == name) null all).value);
		}}
	"""
        ).render
