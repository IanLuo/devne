{ ss, nixpkgs, python_units, system, name, version, lib }:
let
  wrapInUnit = ss.lib.wrapInUnit;
  sslib = ss.lib;
  metadata = { inherit name version; };


  nixpkgs-fmg = (sslib.defineUnit {
    name = "nixpkgs-fmg";
    version = "0.0.1";
    source = nixpkgs.nixpkgs-fmt;
    instantiate = null;
    actions = null;
    listener = null;
  });


  jsonfmt = (sslib.defineUnit {
    name = "jsonfmt";
    version = "0.0.1";
    source = nixpkgs.jsonfmt;
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
    nixpkgs-fmg
    jsonfmt
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
	