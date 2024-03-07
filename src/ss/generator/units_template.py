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

        super_class = super()

        def render_unit(name, attrs):
            if attrs is None:
                return StrRender(f"""{name.replace(".","_")} = {name};""").render
            else:
                return StrRender(
                    f"""
                    {name.replace(".","_")} = {name} {{
                        {super_class.render_map(self.configure, attrs)}
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

        all = [ {space.join(names)}];

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
