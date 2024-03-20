{ system, name, version, lib, sstemplate, pkgs, other }:
let
  units = import sstemplate { inherit pkgs; };
  wrapInUnit = units.sslib.wrapInUnit;
  metadata = { inherit name version; };


  sstemplate_db_postgres = (wrapInUnit {
    drv = (sstemplate.db.postgres
      {
        username = "ss_db";
        password = "admin";
        database = "password";
      }
    );
  });


  sstemplate_language_python = (wrapInUnit {
    drv = (sstemplate.language.python
      {
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
      }
    );
  });


  sstemplate_language_pytest = (wrapInUnit {
    drv = (sstemplate.language.pytest
      {
        python = sstemplate_language_python.value;
      }
    );
  });


  sstemplate_language_pythonRunnablePackage = (wrapInUnit {
    drv = (sstemplate.language.pythonRunnablePackage
      {
        name = metadata.name;
        version = metadata.version;
        src = ../.;
        format = "wheel";
        python = sstemplate_language_python.value;
        buildInputs = sstemplate_language_python.libs-default;
      }
    );
  });

  pkgs_nodePackages_pyright = (wrapInUnit { drv = pkgs.nodePackages.pyright; });
  pkgs_nixpkgs-fmt = (wrapInUnit { drv = pkgs.nixpkgs-fmt; });
  other_some1 = (wrapInUnit { drv = other.some1; });

  other_some2 = (wrapInUnit {
    drv = (other.some2
      {
        param1 = "1";
      }
    );
  });


  all = [
    sstemplate_db_postgres
    sstemplate_language_python
    sstemplate_language_pytest
    sstemplate_language_pythonRunnablePackage
    pkgs_nodePackages_pyright
    pkgs_nixpkgs-fmt
    other_some1
    other_some2
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
	