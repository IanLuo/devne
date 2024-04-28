{ ss, nixpkgs, system, name, version, lib }:
let
  wrapInUnit = ss.lib.wrapInUnit;
  sslib = ss.lib;
  metadata = { inherit name version; };


  python = (sslib.defineUnit {
    name = "python";
    versoin = "0.0.1";
    source = nixpkgs.python310;
    initialize = "python -m venv .venv source .venv/bin/activate";
    actions = null;
    listener = null;
  });


  poetry = (sslib.defineUnit {
    name = "poetry";
    versoin = "0.0.1";
    source = nixpkgs.poetry;
    initialize = null;
    actions = null;
    listener = null;
  });


  pyright = (sslib.defineUnit {
    name = "pyright";
    versoin = "0.0.1";
    source = nixpkgs.nodePackages.pyright;
    initialize = null;
    actions = null;
    listener = null;
  });


  nixpkgs-fmg = (sslib.defineUnit {
    name = "nixpkgs-fmg";
    versoin = "0.0.1";
    source = nixpkgs.nixpkgs-fmt;
    initialize = null;
    actions = null;
    listener = null;
  });


  database = (sslib.defineUnit {
    name = "database";
    versoin = "0.0.1";
    source = nixpkgs.postgres;
    initialize = null;
    actions = null;
    listener = null;
  });


  cache = (sslib.defineUnit {
    name = "cache";
    versoin = "0.0.1";
    source = nixpkgs.redis;
    initialize = null;
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
	
