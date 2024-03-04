
	{ sstemplate, system, name, version, lib, pkgs }:
		let
		template = import sstemplate { inherit system pkgs; };

		all = lib.lists.filter (x: x.isUnit) (
			[
				(
		# TODO: wrap every dev inside a unit
			pkgs.nodePackages.pyright.overrideAttrs {  }
		)
			]
			++
			[
				(
				template.db.postgres { username = "ss_db";
password = "admin";
database = "password"; }
				) (
				template.language.python { pythonVersion = "python310";
libs-default = ["typer" "pynvim" "pyyaml" "rich" "jsonpath-ng" "requests" "black" "{'flit': {'^git': {'url': 'https://www.github.com/xxxxx', 'rev': 'xxxxx'}}}"];; }
				) (
				template.language.pytest { python = "None"; }
				) (
				template.language.pythonRunnablePackage { name = "ss";
version = "0.0.1";
src = "../.";
format = "pyproject";
python = "None";
buildInputs = "None~>libs-default"; }
				)
			]);

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
	