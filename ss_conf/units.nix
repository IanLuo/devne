{ sstemplate, system, name, version, lib, pkgs }:
let 
  template = import sstemplate { inherit system pkgs; };
  language = template.language;
  powers = template.powers;

  python = language.python {
    pythonVersion = "python310";
    name = name;
    src = ../.;
    version = version;
    buildInputs = [ "typer" "pynvim" "pyyaml" "rich" "jsonpath-ng" "requests" "black" "flit" ];
  };



  powers_db_postgres = powers.db.postgres {
    username = "ss_db";
    password = "admin";
    database = "password";
  };
        

  all = [ powers_db_postgres python ];

  startScript = ''
    export SS_PROJECT_BASE=$PWD
  '';
in {
  inherit all;
  scripts = builtins.concatStringsSep "\n" ([ startScript ] ++ map (unit: unit.script) all);
  packages = lib.attrsets.genAttrs 
               (map 
                  (x: x.package.pname) 
                  (lib.lists.filter (x: lib.attrsets.hasAttrByPath ["package"] x && x.package != null) all)) 
               (name: 
                (lib.lists.findFirst (x: x.package != null && x.package.pname == name) null all).package) ;
}
