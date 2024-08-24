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
            {LINE_BREAK.join([f"{name} = {self.renderer.render_value(name=name, value=action, as_nix_code=True)};" for name, action in actions.items()])}            
        }};
        '''

    def render_onstart(self, onstart: dict) -> str:
        return f'''
            {self.blueprint.name}_onstart= { self.renderer.render_value(name='onstart', value=onstart) };
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
            { self.render_onstart(self.blueprint.onstart or {}) }

            all = [ {line_break.join(names)}];
            all_attr = {{ inherit { space.join(names) }; }};

            unitsProfile = lib.attrsets.mapAttrs 
                (name: unit: 
                    {{
                        path = unit;
                        actions = if unit ? actions && unit.actions != null then unit.actions else {{}};
                        onstart = if unit ? onstart && unit.actions != null then unit.onstart else {{}};
                    }}                    
                ) 
                all_attr;

            currentProfile = {{
                 {self.blueprint.name} = {{
                     inherit actions;
                }};
            }};

            mapShs = sh:
                if builtins.isList sh then 
                    map (x: mapShs x) sh 
                else 
                    ["source ${{sh}}"];

            load-profile = pkgs.writeScriptBin "load_profile" ''
                echo '${{builtins.toJSON ( unitsProfile // currentProfile)}}'
            '';

            onStartScript = lib.strings.concatStringsSep
                "\n" 
                (lib.flatten 
                  (
                    (map 
                      (x: mapShs x.onstart) 
                      (lib.filter (unit: unit ? onstart && unit.onstart != null) all) ++ (mapShs {self.blueprint.name}_onstart)
                    )
                  )
                );

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
