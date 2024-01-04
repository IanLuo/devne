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
    pythonVersion = "python310";
    libs-default = [ "typer" "pynvim" "pyyaml" "rich" "jsonpath-ng" "requests" "black" "flit" ];
  };
        


  language_pytest = language.pytest {
    python = if language_python.value == null then language_python else language_python.value;
  };
        


  language_pythonRunnablePackage = language.pythonRunnablePackage {
    name = "ss";
    version = "0.0.1";
    src = ../.;
    format = "pyproject";
    python = if language_python.value == null then language_python else language_python.value;
    buildInputs = language_python.libs-default;
  };
        

  all = lib.lists.filter (x: x.isUnit) [ db_postgres language_python language_pytest language_pythonRunnablePackage ];

  startScript = ''
    export SS_PROJECT_BASE=$PWD
  '';
in {
  inherit all;
  scripts = builtins.concatStringsSep "\n" ([ startScript ] ++ map (unit: unit.script) all);
  packages = lib.attrsets.genAttrs 
               (map 
                  (x: x.value.pname) 
                  (lib.lists.filter (x: x.isPackage) all))

               (name: 
                (lib.lists.findFirst (x: x.isPackage && x.value.pname == name) null all).value);
}
