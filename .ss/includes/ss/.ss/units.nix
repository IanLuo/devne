
	{  nixpkgs,system,name,version,lib }:
		let
            wrapInUnit = ss.lib.wrapInUnit;
            sslib = ss.lib;
            metadata = { inherit name version; };

            

            all = [ ];

            startScript = ''
                export SS_PROJECT_BASE=$PWD
            '';
		in {
		inherit all;
		scripts = builtins.concatStringsSep "\n" ([ startScript ] ++ map (unit: unit.script) all);
        dependencies = all; 
		}
	