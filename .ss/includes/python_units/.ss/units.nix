
	{  ss,nixpkgs,system,name,version,lib }:
		let
            wrapInUnit = ss.lib.wrapInUnit;
            sslib = ss.lib;
            metadata = { inherit name version; };

            
                python = (sslib.defineUnit {
                    name = "python";
                    version = null;
                    source=nixpkgs.python310;
instantiate=
                ''python -m venv .venv
source .venv/bin/activate
''
            ;
actions=null;
listener=null;
                });
                

                poetry = (sslib.defineUnit {
                    name = "poetry";
                    version = null;
                    source=nixpkgs.poetry;
instantiate=null;
actions=
                {
                    install = "poetry install";
add = "poetryh add";
list = "poetry list";
build = "poetry build";
                }
            ;
listener=null;
                });
                

                pyright = (sslib.defineUnit {
                    name = "pyright";
                    version = null;
                    source=nixpkgs.nodePackages.pyright;
instantiate=null;
actions=null;
listener=null;
                });
                

            all = [ python
poetry
pyright];

            startScript = ''
                export SS_PROJECT_BASE=$PWD
            '';
		in {
		inherit all;
		scripts = builtins.concatStringsSep "\n" ([ startScript ] ++ map (unit: unit.script) all);
        dependencies = all; 
		}
	