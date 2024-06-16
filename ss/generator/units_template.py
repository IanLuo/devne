from ..configure.blueprint import Blueprint
from .template import Template
from dataclasses import dataclass

@dataclass
class UnitsTemplate(Template):
    blueprint: Blueprint

    def render(self) -> str:
        line_break = "\n"

        names = list(map(lambda x: x.replace(".", "_"), self.blueprint.units.keys()))

        super_class = super()

        version_str = lambda value: f'version = \"{value.get("version")}\";' if value.get("version", None) is not None else ''

        def render_unit(name, value):
            return f"""
                {name} = (sslib.defineUnit {{
                    name = "{name}";
                    {version_str(value)}
                    {line_break.join([f'{key}={super_class.render_value(value)};' for key, value in value.items()])}
                }});
                """

        render_units_in_sources = line_break.join(
            [render_unit(name, value) for name, value in self.blueprint.units.items()]
        )

        default_imports = ["system", "name", "version", "lib" ]
        all_import = list(self.blueprint.includes.keys()) + default_imports

        return f"""
	{{  {','.join(all_import) } }}:
		let
            wrapInUnit = ss.lib.wrapInUnit;
            sslib = ss.lib;
            metadata = {{ inherit name version; }};

            {render_units_in_sources}

            all = [ {line_break.join(names)}];

            startScript = ''
                export SS_PROJECT_BASE=$PWD
            '';
		in {{
		inherit all;
		scripts = builtins.concatStringsSep "\\n" ([ startScript ] ++ map (unit: unit.script) all);
        dependencies = all; 
		}}
	"""
