{
  description = "devlopment environment with 1 command";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";

    ss = {
      url = "path:/Users/ianluo/Documents/apps/templates";
    };


    nixpkgs = {
      url = "github:NixOS/nixpkgs/nixos-23.11";
    };

  };

  outputs = { self, flake-utils, flake-parts, ss, nixpkgs }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};

        version = "0.0.1";
        name = "ss";

        units = pkgs.callPackage ./units.nix { inherit name version ss; nixpkgs = pkgs; };
      in
      {
        devShells = with pkgs; {
          default = mkShell {
            name = name;
            version = version;
            packages = units.dependencies;

            shellHook = ''
              ${units.scripts}
            '';
          };
        };
      });
}
      