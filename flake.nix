{
  description = "A very basic flake";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  inputs.nixpkgs.inputs.nixpkgs.follows = "nixpkgs";

  inputs.flake-utils.url = "github:numtide/flake-utils";

  inputs.devne-template.url = "git+file:///Users/ianluo/Documents/apps/templates";
  inputs.devne-template.inputs.nixpkgs.follows = "nixpkgs";

  outputs = { self, nixpkgs, flake-utils, devne-template }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        native = devne-template.native.${system};

        pythonCliApp = native.python {
          pythonVersion = "python38";
          src = ./.;
        };
        version = "0.0.1";
        name = "cli";
      in
      {
        devShells = with pkgs; {
          default = mkShell {
            name = name;
            version = version;
            buildInputs = [
              pythonCliApp
            ];

            shellHook = ''
              pythonCliApp.python --version
            '';
            };
        };

        packages = {
          default = pkgs.poetry2nix.mkPoetryApplication {
            projectDir = ./.;
          };
        };

      });
}
