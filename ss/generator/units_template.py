from .template import Template

class UnitsTemplate(Template):
    def __init__(self, blueprint):
        super().__init__(blueprint)

    def render(self) -> str:
        line_break = "\n"

        names = list(map(lambda x: x.replace(".", "_"), self.blueprint.units.keys()))

        version_str = lambda value: f'\"{value.get("version")}\"' if value.get("version", None) is not None else 'null'

        def render_unit(name, value):
            return f"""
                {name} = (sslib.defineUnit {{
                    name = "{name}";
                    version = {version_str(value)};
                    {line_break.join([f'{key}={self.render_value(value)};' for key, value in value.items()])}
                }});
                """

        render_units_in_sources = line_break.join(
            [render_unit(name, value) for name, value in self.blueprint.units.items()]
        )

        default_imports = ["system", "name", "version", "lib" ]
        all_import = [ item[0] for item in self.includes if item[1] is not None ] + default_imports

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
