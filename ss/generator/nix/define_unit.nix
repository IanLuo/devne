{ pkgs, stdenv, lib }:

{ name
# the source of the unit, can be a git repo, or a local path
, source
# env vars that will be set by this unit
, envs ? null, onstart ? null, install ? "", actions ? null, ... }@inputs:

let
  findOutType = x:
    if lib.isAttrs x then
      if lib.hasAttr "out" x then "drv" else "attrs"
    else if lib.isPath x then
      "path"
    else
      "material";

  installScriptForSource = source:
    let sourceType = findOutType source;

    in if sourceType == "drv" then ''
      mkdir -p $out
      ln -s ${source}/* $out
    '' else if sourceType == "path" then ''
      mkdir -p $out
      cp -r ${source}/* $out
    '' else ''
      mkdir -p $out
    '';

  installPhaseScript = installScriptForSource inputs.source;

  passthrus_ = {
    isUnit = true;
  } // (lib.attrsets.removeAttrs inputs [ "source" "install" ]);

in let
  drv = stdenv.mkDerivation {
    name = name;
    src = inputs.source;
    dontConfigure =
      if (lib.attrsets.hasAttrByPath [ "dontConfigure" ] inputs) then
        inputs.dontConfigure
      else
        false;
    installPhase = installPhaseScript;
    passthru = passthrus_;
  };
in drv
