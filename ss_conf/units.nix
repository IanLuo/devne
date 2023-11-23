{ sstemplate, system, name, version, lib, pkgs }:
let 
  native = sstemplate.native.${system};
  powers = sstemplate.powers.${system};

  python = native.python {
    pythonVersion = "python310";
    name = name;
    src = ../.;
    version = version;
    buildInputs = ps: with ps; [ typer pynvim pyyaml rich jsonpath-ng requests black ];
  };



  powers_db_postgres = powers.db.postgres {
    username = "test_user";
    password = "test_password";
    database = "test_database";
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
                  (x: x.buildapp.pname) 
                  (lib.lists.filter (x: lib.attrsets.hasAttrByPath ["buildapp"] x && x.buildapp != null) all)) 
               (name: 
                (lib.lists.findFirst (x: x.buildapp != null && x.buildapp.pname == name) null all).buildapp) ;
}
