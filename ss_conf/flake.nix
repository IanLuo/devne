{
  description = "devlopment environment with 1 command";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";

    ss = {
      url = "path:///Users/ianluo/Documents/apps/templates";
      flake = true;
    };


    python_units = {
      url = "git+https://github.com/IanLuo/python_units?rev=5563efcf1f9226796eaf2cec3e4f32498ba0a19e";
      flake = true;
    };


    nixpkgs = {
      url = "git+https://github.com/NixOS/nixpkgs?rev=ed5f4b938fa96aa6ad20fff3b04bd96bf5abb3f9";
      flake = true;
    };

  };

  outputs = { self, flake-utils, flake-parts, ss, python_units, nixpkgs }:
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
            packages = units.dependencies;

            shellHook = ''
              ${units.scripts}
            '';
          };
        };
      });
}
      