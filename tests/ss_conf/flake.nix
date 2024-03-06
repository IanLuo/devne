
{
  description = "project description";

  inputs.nixpkgs = {
    url = "github:NixOS/nixpkgs?rev=the_rev_of_pkgs";
    inputs.nixpkgs.follows = "nixpkgs";
  };

  inputs.flake-utils.url = "github:numtide/flake-utils";

  inputs.sstemplate.url = "github:ianluo/ss-templates";
  inputs.sstemplate.inputs.nixpkgs.follows = "nixpkgs";

  outputs = { self, nixpkgs, flake-utils, sstemplate }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        units = pkgs.callPackage ./units.nix { inherit sstemplate name version system; };
      in
      {
        devShells = with pkgs; {
          default = mkShell {
            name = name;
            version = version;
            buildInputs = units.all;

            shellHook = ''
              ${units.scripts}
            '';
          };
        };

        packages = units.packages;
      });
}
