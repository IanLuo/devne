{
  description = "devlopment environment with 1 command";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";

    ss = {
      url = "path:///Users/ianluo/Documents/apps/templates";
      flake = true;
    };


    nixpkgs = {
      url = "git+https://github.com/NixOS/nixpkgs?rev=ec35143a579ad4e5efc198e4dbe3f0a2d9139b04";
      flake = true;
    };

  };

  outputs = { self, flake-utils, ss, nixpkgs }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        version = "0.0.1";
        name = "ss";

        units = pkgs.callPackage ./units.nix { inherit name version ss; nixpkgs = pkgs; };
      in
      {
        libs = units;
        devShells = with pkgs; {
          default = mkShell {
            name = name;
            version = version;
            buildInputs = units.dependencies;

            shellHook = ''
              ${units.scripts}
            '';
          };
        };
      });
}
      
