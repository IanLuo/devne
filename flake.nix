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

        version = "0.0.1";
        name = "ss-cli";

        native = devne-template.native.${system};
        powers = devne-template.powers.${system};


        pythonCliApp = native.python {
          pythonVersion = "python38";
          name = name;
          version = version;
        };

        postgres = powers.db.postgres {
          database = "ss_cli";
          folder = "postgres";        
        };

        units = [
          pythonCliApp
          postgres
        ];

        update-template = pkgs.writeScriptBin "update_template" ''
          nix flake lock --update-input devne-template
        '';
      in
      {
        devShells = with pkgs; {
          default = mkShell {
            name = name;
            version = version;
            buildInputs = [
              update-template
            ] ++ units;

            shellHook = ''
              python --version

              ${builtins.concatStringsSep "\n" (map (unit: unit.script) units)}
            '';
          };
        };

        packages.default = pythonCliApp.buildapp {};

      });
}
