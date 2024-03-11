{ sstemplate, system, name, version, lib, pkgs }:
let
  units = import sstemplate { inherit system pkgs; };
  wrapInUnit = units.sslib.wrapInUnit;
  metadata = { inherit name version; };


  units_db_postgres = (wrapInUnit {
    drv = (units.db.postgres {
      username = "ss_db";
      password = "admin";
      database = "password";
    });
  });


  units_language_python = (wrapInUnit {
    drv = (units.language.python {
      pythonVersion = "python310";
      libs-default = [
        "typer"
        "pynvim"
        "pyyaml"
        "rich"
        "jsonpath-ng"
        "requests"
        "black"
        "flit"
      ];
    });
  });


  units_language_pytest = (wrapInUnit {
    drv = (units.language.pytest { python = units_language_python.value; });
  });


  units_language_pythonRunnablePackage = (wrapInUnit {
    drv = (units.language.pythonRunnablePackage {
      name = metadata.name;
      version = metadata.version;
      src = ../.;
      format = "pyproject";
      python = units_language_python.value;
      buildInputs = units_language_python.libs-default;
    });
  });

  pkgs_nodePackages_pyright = (wrapInUnit { drv = pkgs.nodePackages.pyright; });
  pkgs_nixpkgs-fmt = (wrapInUnit { drv = pkgs.nixpkgs-fmt; });

  all = [
    units_db_postgres
    units_language_python
    units_language_pytest
    units_language_pythonRunnablePackage
    pkgs_nodePackages_pyright
    pkgs_nixpkgs-fmt
  ];

  startScript = ''
    export SS_PROJECT_BASE=$PWD
  '';
in
{
  inherit all;
  scripts = builtins.concatStringsSep "\n" ([ startScript ] ++ map (unit: unit.script) all);
  packages = lib.attrsets.genAttrs
    (map
      (x: x.value.pname)
      (lib.lists.filter (x: x.isPackage) all))

    (name:
      (lib.lists.findFirst (x: x.isPackage && x.value.pname == name) null all).value);
}
	