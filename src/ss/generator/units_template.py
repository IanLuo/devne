from ..configure.configure import Configure
from .template import Template
from dataclasses import dataclass
from functools import reduce


@dataclass
class UnitsTemplate(Template):
    configure: Configure

    def render(self) -> str:
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
                [units_in_source(source_name) for source_name in sources.keys()],
            ),
            {}
        )

        names = list(map(lambda x: x.replace(".", "_"), render_sources.keys()))

        super_class = super()

        def render_unit(name, value):
            if value is None:
                return f"""{name.replace(".","_")} = (wrapInUnit {{ drv = {name}; }});"""
            else:
                return f"""
                    {name.replace(".","_")} = (wrapInUnit {{
                        drv = ({name} {super_class.render_value(self.configure, value)});
                    }});
                    """

        render_units_in_sources = line_break.join(
            [render_unit(name, value) for name, value in render_sources.items()]
        )

        return f"""
	{{ system, name, version, lib, {','.join(self.configure.sources.keys())} }}:
		let
            units = import sstemplate {{ inherit pkgs; }};
            wrapInUnit = units.sslib.wrapInUnit;
            metadata = {{ inherit name version; }};

            {render_units_in_sources}

            all = [ {line_break.join(names)}];

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
