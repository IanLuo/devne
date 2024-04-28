{
  description = "devlopment environment with 1 command";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";

    ss = {
      url = "https://github.com/IanLuo/ss-templates";
    };


    nixpkgs = {
      url = "https://github.com/NixOS/nixpkgs/nixpkgs-unstable";
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

        packages = units.packages;
      });
}
      