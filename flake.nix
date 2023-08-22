{
  description = "A very basic flake";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.nixpkgs.inputs.nixpkgs.follows = "nixpkgs";

  inputs.flake-utils.url = "github:numtide/flake-utils";

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        pythonInUse = pkgs.python38;

        pythonWebPkgs = pythonInUse.withPackages (ps: with ps; [
          flask
        ]);

        pythonCliPkgs = pythonInUse.withPackages (ps: with ps; [
          typer
        ]);
      in
      {
        devShells = with pkgs; {
          default = mkShell {
            buildInputs = [
              pythonWebPkgs
            ];
          };
          cli = mkShell {
            buildInputs = [
              pythonCliPkgs
            ];
          };
        };

        packages = {
          default = pkgs.writeText "hello.txt" "Hello, world!";
        };
      });
}
