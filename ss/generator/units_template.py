from ss.configure.blueprint import Blueprint
from ss.configure.schema import LINE_BREAK, SPACE
from .renderer import Renderer

class UnitsTemplate:
    def __init__(self, blueprint: Blueprint):
        self.blueprint = blueprint 
        self.renderer = Renderer(blueprint=blueprint)    

    def render_unit(self, name, unit):
        params = self.renderer.extract_params(unit=unit)

        if self.blueprint.is_root_blueprint:
            return f"""
                {name} = (
                  {self.renderer.render_call_father(name=name, unit=unit, blueprint=self.blueprint)}
                sslib.defineUnit
                {{
                    name = "{name}";
                    {self.renderer.render_unit(unit=unit)}
                }});
            """
        else:
            return f"""{name} ={{ 
                {",".join([f"{key} ? {self.renderer.render_value(name, value)}" for key, value in params.items()])}
            }}: {{
              {self.renderer.render_unit(unit=unit)}
           }};""" 

    def render_actions(self, actions: dict) -> str:
        return f'''
        actions = {{
            {LINE_BREAK.join([f"{name} = {self.renderer.render_value(name=name, value=action)};" for name, action in actions.items()])}            
        }};
        '''
        
    def render(self) -> str:
        line_break = "\n"
        space = " "

        names = list(map(lambda x: x.replace(".", "_"), self.blueprint.units.keys()))

        render_units_in_sources = line_break.join(
            [self.render_unit(name, value) for name, value in self.blueprint.units.items()]
        )

        default_imports = ["pkgs", "system", "name", "version", "lib" ]
        all_import = [ item[0] for item in self.renderer.includes if item[1] is not None ] + default_imports


        return f"""
	{{  {','.join(all_import) } }}:
		let
            wrapInUnit = templates.lib.wrapInUnit;
            sslib = templates.lib;
            metadata = {{ inherit name version; }};

            {render_units_in_sources}

            { self.render_actions(self.blueprint.actions or {}) }

            all = [ {line_break.join(names)}];
            all_attr = {{ inherit { space.join(names) }; }};

            units_profile = lib.attrsets.mapAttrs 
                (name: unit: 
                    {{
                        path = unit;
                        actions = unit.actions;
                    }}                    
                ) 
                all_attr;

            current_profile = {{
                 {self.blueprint.name} = {{
                    actions = actions;
                }};
            }};

            load-profile = pkgs.writeScriptBin "load_profile" ''
                echo '${{builtins.toJSON (units_profile // current_profile)}}'
            '';

            onStartScript = lib.strings.concatStringsSep
                " " 
                (map (x: x.onstart) (lib.filter (unit: ({{ onstart = null;}} // unit).onstart != null) all));

            startScript = ''
                export SS_PROJECT_BASE=$PWD
            '';

            funcs = [ load-profile ];
            

		in {{
		inherit all all_attr funcs actions;
		scripts = builtins.concatStringsSep "\\n" [ onStartScript ];
        dependencies = all; 
		}}
	"""
