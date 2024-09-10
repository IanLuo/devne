{ pkgs, ... }:

let
  defineUnit = pkgs.callPackage ./define_unit.nix { };
  env = pkgs.callPackage ./env.nix { };
in with pkgs; { inherit defineUnit env; }
