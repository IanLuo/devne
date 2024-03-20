{
  description = "devlopment environment with 1 command";

  inputs.flake-utils.url = "github:numtide/flake-utils";


  sstemplate = {
    url = "";
  };


  nixpkgs = {
    url = "github:ianluo/ss-templates";
  };


  other = {
    url = "";
  };


  outputs = { self, flake-utils, sstemplate, nixpkgs, other }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };

        version = "0.0.1";
        name = "ss";

        units = pkgs.callPackage ./units.nix { inherit sstemplate name version system; };
      in
      {
        devShells = with pkgs; {
          default = mkShell {
            name = name;
            version = version;
            buildInputs = (map (x: x.value) units.all);

            shellHook = ''
              ${units.scripts}
            '';
          };
        };

        packages = units.packages;
      });
}
      