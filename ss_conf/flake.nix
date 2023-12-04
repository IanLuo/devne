{
  description = "devlopment environment with 1 command";

  inputs.nixpkgs = {
    url = "github:NixOS/nixpkgs?rev=f895a4ef0f01f9d2af2370533829c4f03ec408f4";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  inputs.flake-utils.url = "github:numtide/flake-utils";

  inputs.sstemplate.url = "git+file:///Users/ianluo/Documents/apps/templates";
  inputs.sstemplate.inputs.nixpkgs.follows = "nixpkgs";

  outputs = { self, nixpkgs, flake-utils, sstemplate }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        metadata = import ./flake_metadata.nix;
        version = metadata.version;
        name = metadata.name;

        units = pkgs.callPackage ./units.nix { inherit sstemplate name version system pkgs; };
        deps = pkgs.callPackage ./deps.nix { };
      in
      {
        devShells = with pkgs; {
          default = mkShell {
            name = name;
            version = version;
            buildInputs = units.all ++ deps; 

            shellHook = ''
              ${units.scripts}
            '';
          };
        };

        packages = units.packages;
      });
}
