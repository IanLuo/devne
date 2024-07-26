{ pkgs ? import <nixpkgs> { } }:
let
  ss = pkgs.callPackage /Users/ianluo/Documents/apps/ss/.ss/includes/ss/ss.nix { };
  python_units = pkgs.callPackage /Users/ianluo/Documents/apps/ss/.ss/includes/python_units/ss.nix { };
  nixpkgs = pkgs.callPackage /nix/store/jx2p25acvlwdl87cl237rk23qgyn35h7-nixpkgs-b729601/default.nix { };
  name = "ss";
  version = "0.0.1";
  units = pkgs.callPackage ./unit.nix { inherit ss python_units nixpkgs; };
in
pkgs.mkShell {
  name = name;
  version = version;
  buildInputs = [
    units
  ];

  shellHook = ''
    echo "Welcome to ${name} shell"
    ${units.scripts}
  '';
}
        
