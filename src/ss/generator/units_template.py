from ..configure.configure import Configure
from .template import Template
from dataclasses import dataclass
from typing import List
from .str_render import StrRender
from ..configure.functions.git_repo import GitRepo
from functools import reduce


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
        elif None:
            return nil
        else:
            return str(value)

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
        line_break = "\n"
        sources = self.configure.sources

        units_in_source = lambda source_name: {
            f"{source_name}.{unit_instance.definition.name}": unit_instance.definition.attrs
            for unit_instance in self.configure.units_for_source(source_name)
        }

        render_sources = reduce(
            lambda a, b: {**a, **b},
            filter(
                lambda x: len(x) > 0,
                [units_in_source(source_name) for source_name in sources],
            ),
        )

        names = list(map(lambda x: x.replace(".", "_"), render_sources.keys()))

        def render_unit(name, attrs):
            if attrs == None:
                return StrRender(
                    f"""
                    {name.replace(".","_")} = {name};
                """
                ).render
            else:
                return StrRender(
                    f"""
                    {name.replace(".","_")} = {name} {{
                        {line_break.join([f'{name} = "{self._render_value(value)}";' for name, value in attrs.items()])}
                    }};
                """
                ).render

        render_units_in_sources = line_break.join(
            [render_unit(name, attrs) for name, attrs in render_sources.items()]
        )

        return StrRender(
            f"""
	{{ sstemplate, system, name, version, lib, pkgs }}:
		let
		template = import sstemplate {{ inherit system pkgs; }};

        {render_units_in_sources}

        all = [ {space.join(names)}]

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
