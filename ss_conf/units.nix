{ sstemplate, system, name, version, lib, pkgs }:
let 
  template = import sstemplate { inherit system pkgs; };
  language = template.language;
  db = template.db;



  db_postgres = db.postgres {
    username = "ss_db";
    password = "admin";
    database = "password";
  };
        


  language_python = language.python {
    name = "ss";
    version = "0.0.1";
    src = ../.;
    buildFormat = "pyproject";
    pythonVersion = "python310";
    libs-default = [ "typer" "pynvim" "pyyaml" "rich" "jsonpath-ng" "requests" "black" "flit" ];
  };
        


  language_pytest = language.pytest {
    python = language_python.value;
  };
        

  all = [ db_postgres language_python language_pytest ];

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
                (lib.lists.findFirst (x: lib.attrsets.hasAttrByPath ["package"] x &&  x.package != null && x.package.pname == name) null all).package);
}
