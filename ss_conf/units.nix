
	{ sstemplate, system, name, version, lib, pkgs }:
		let
		template = import sstemplate { inherit system pkgs; };

        
            units_db_postgres = units.db.postgres {
                username = "ss_db";
password = "admin";
database = "password";
            };
        

            units_language_python = units.language.python {
                pythonVersion = "python310";
libs-default = "["typer" "pynvim" "pyyaml" "rich" "jsonpath-ng" "requests" "black" "{'flit': {'^git': {'url': 'https://www.github.com/xxxxx', 'rev': 'xxxxx'}}}"];";
            };
        

            units_language_pytest = units.language.pytest {
                python = "$language_python";
            };
        

            units_language_pythonRunnablePackage = units.language.pythonRunnablePackage {
                name = "$metadata>name";
version = "$metadata>version";
src = "../.";
format = "pyproject";
python = "$language_python";
buildInputs = "$language_python~>libs-default";
            };
        

            pkgs_nodePackages_pyright = pkgs.nodePackages.pyright {
                
            };
        

        all = [ units_db_postgres units_language_python units_language_pytest units_language_pythonRunnablePackage pkgs_nodePackages_pyright]

		startScript = ''
			export SS_PROJECT_BASE=$PWD
		'';
		in {
		inherit all;
		scripts = builtins.concatStringsSep "\n" ([ startScript ] ++ map (unit: unit.script) all);
		packages = lib.attrsets.genAttrs
					(map
						(x: x.value.pname)
						(lib.lists.filter (x: x.isPackage) all))

					(name:
						(lib.lists.findFirst (x: x.isPackage && x.value.pname == name) null all).value);
		}
	