from ..configure.configure import Configure
from .template import Template
from dataclasses import dataclass

@dataclass
class UnitsTemplate(Template):
  configure: Configure

  def render(self):
    return f'''
{{ sstemplate, system, name, version, lib, pkgs }}:
let
  template = import sstemplate {{ inherit system pkgs; }};
  language = template.language;
  db = template.db;

#UNITS#

  all = lib.lists.filter (x: x.isUnit) #UNITS_REF#;

  startScript = ''
    export SS_PROJECT_BASE=$PWD
  '';
in {{
  inherit all;
  scripts = builtins.concatStringsSep "\n" ([ startScript ] ++ map (unit: unit.script) all);
  packages = lib.attrsets.genAttrs
               (map
                  (x: x.value.pname)
                  (lib.lists.filter (x: x.isPackage) all))

               (name:
                (lib.lists.findFirst (x: x.isPackage && x.value.pname == name) null all).value);
}}
'''
