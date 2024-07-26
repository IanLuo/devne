{ ss, python_units, nixpkgs, system, name, version, lib }:
let
  wrapInUnit = ss.lib.wrapInUnit;
  sslib = ss.lib;
  metadata = { inherit name version; };


  python = (sslib.defineUnit {
    name = "python";
    version = null;
    source = nixpkgs.python310;
    instantiate =
      ''python -m venv .venv
source .venv/bin/activate
poetry install
''
    ;
    actions =
      {
        test = "pytest";
        run = "python -m src.main";
      };
    listener = null;
  });


  poetry = (sslib.defineUnit {
    name = "poetry";
    version = null;
    source = nixpkgs.poetry;
    instantiate = null;
    actions =
      {
        install = "poetry install";
        add = "poetryh add";
        list = "poetry list";
        build = "poetry build";
      };
    listener = null;
  });


  nixpkgs-fmg = (sslib.defineUnit {
    name = "nixpkgs-fmg";
    version = null;
    source = nixpkgs.nixpkgs-fmt;
    instantiate = null;
    actions = null;
    listener = null;
  });


  jsonfmt = (sslib.defineUnit {
    name = "jsonfmt";
    version = null;
    source = nixpkgs.jsonfmt;
    instantiate = null;
    actions = null;
    listener = null;
  });


  database = (sslib.defineUnit {
    name = "database";
    version = null;
    source = nixpkgs.postgresql;
    instantiate = null;
    actions = null;
    listener = null;
  });


  cache = (sslib.defineUnit {
    name = "cache";
    version = null;
    source = nixpkgs.redis;
    instantiate = null;
    actions = null;
    listener = null;
  });


  prefetch-git = (sslib.defineUnit {
    name = "prefetch-git";
    version = null;
    source = nixpkgs.nix-prefetch-git;
    instantiate = null;
    actions = null;
    listener = null;
  });


  all = [
    python
    poetry
    nixpkgs-fmg
    jsonfmt
    database
    cache
    prefetch-git
  ];

  startScript = ''
    export SS_PROJECT_BASE=$PWD
  '';
in
{
  inherit all;
  scripts = builtins.concatStringsSep "\n" ([ startScript ] ++ map (unit: unit.script) all);
  dependencies = all;
}
	