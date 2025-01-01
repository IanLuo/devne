{ pkgs, lib, ... }:

let
  defineUnit = pkgs.callPackage ./define_unit.nix { };
  env = pkgs.callPackage ./env.nix { };

  # used to execute sh commands, if the value is a shell, just run it, if it is a list, run each command one by one
  mapShs = sh:
    if builtins.isList sh then map (x: mapShs x) sh else [ "source ${sh}" ];

  onStartScript = units: onstart:
    lib.strings.concatStringsSep "\n" (lib.flatten ((map (x: mapShs x.onstart)
      (lib.filter (unit: unit ? onstart && unit.onstart != null) units)
      ++ (mapShs onstart))));

  getUnitsFromImportedConfigures = importedSSConfigures:
    lib.attrsets.mapAttrs (name: include: {
      "units" = (lib.lists.groupBy' (x: y: x // y) { } (x: x.name)
        (map (unit: lib.attrsets.removeAttrs unit [ "source" ]) include.all));
    }) importedSSConfigures;

  getOnstartFromImportedConfigures = importedSSConfigures:
    lib.attrsets.mapAttrs (name: include: { "onstart" = include.onstart; })
    importedSSConfigures;

  getActionsFromImportedConfigures = importedSSConfigures:
    lib.attrsets.mapAttrs (name: include: { "actions" = include.actions; })
    importedSSConfigures;

  getServicesFromImportedConfigures = importedSSConfigures:
    lib.attrsets.mapAttrs (name: include: { "services" = include.services; })
    importedSSConfigures;

in with pkgs; {
  inherit defineUnit env mapShs onStartScript getUnitsFromImportedConfigures
    getOnstartFromImportedConfigures getActionsFromImportedConfigures
    getServicesFromImportedConfigures;
}
