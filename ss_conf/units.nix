{ ss, nixpkgs, system, name, version, lib }:
let
  wrapInUnit = ss.lib.wrapInUnit;
  sslib = ss.lib;
  metadata = { inherit name version; };


  python = (sslib.defineUnit {
    name = "python";
    version = "0.0.1";
    source = nixpkgs.python310;
    instantiate =
      ''python -m venv .venv
source .venv/bin/activate
''
    ;
    actions = null;
    listener = null;
  });


  poetry = (sslib.defineUnit {
    name = "poetry";
    version = "0.0.1";
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


  pyright = (sslib.defineUnit {
    name = "pyright";
    version = "0.0.1";
    source = nixpkgs.nodePackages.pyright;
    instantiate = null;
    actions = null;
    listener = null;
  });


  nixpkgs-fmg = (sslib.defineUnit {
    name = "nixpkgs-fmg";
    version = "0.0.1";
    source = nixpkgs.nixpkgs-fmt;
    instantiate = null;
    actions = null;
    listener = null;
  });


  database = (sslib.defineUnit {
    name = "database";
    version = "0.0.1";
    source = nixpkgs.postgresql;
    instantiate = null;
    actions = null;
    listener = null;
  });


  cache = (sslib.defineUnit {
    name = "cache";
    version = "0.0.1";
    source = nixpkgs.redis;
    instantiate = null;
    actions = null;
    listener = null;
  });


  all = [
    python
    poetry
    pyright
    nixpkgs-fmg
    database
    cache
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
	
