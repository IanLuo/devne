{ pkgs ? import <nixpkgs> { } }:
let
  ss = pkgs.importFlake /nix/store/l1q8ki2nm5pcyxs1gk6zd7c9r3v4bz8f-source/flake.nix { };
  nixpkgs = pkgs.callPackage /nix/store/jx2p25acvlwdl87cl237rk23qgyn35h7-nixpkgs-b729601/default.nix { };
  name = "ss";
  version = "0.0.1";
  units = pkgs.callPackage ./unit.nix { inherit ss nixpkgs; };
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
        