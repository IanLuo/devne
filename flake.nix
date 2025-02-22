{
  description = "nix flake installer for SS";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
  };

  outputs = { self, nixpkgs }:
    let
      # Helper function to create package for each system
      forAllSystems = nixpkgs.lib.genAttrs nixpkgs.lib.systems.flakeExposed;

      # Package builder for each system
      makePkgs = system:
        let
          pkgs = import nixpkgs { inherit system; };
          python = pkgs.python312;
          pythonPackages = python.pkgs;
        in {
          default = pythonPackages.buildPythonApplication {
            pname = "ss";
            version = "0.1.0";
            src = ./.;

            format = "pyproject";

            nativeBuildInputs = with pythonPackages; [
              poetry-core
            ];

            propagatedBuildInputs = with pythonPackages; [
              typer
              pyyaml
              pytest
              jsonpath-ng
              pexpect
              plumbum
            ];

            doCheck = false;

            postInstall = ''
              mkdir -p $out/bin
              cat > $out/bin/ss << EOF
              #!${pkgs.bash}/bin/bash
              export PYTHONPATH=$out/lib/python${python.pythonVersion}/site-packages:\$PYTHONPATH
              exec ${python}/bin/python -m ss.main "\$@"
              EOF
              chmod +x $out/bin/ss
            '';

            meta = with pkgs.lib; {
              description = "super start";
              homepage = "https://github.com/ianluo/ss";
              license = licenses.mit;
              platforms = platforms.all;
            };
          };
        };

      # Apps builder for each system
      makeApps = system: {
        default = {
          type = "app";
          program = "${self.packages.${system}.default}/bin/ss";
        };
      };
    in {
      packages = forAllSystems makePkgs;
      apps = forAllSystems makeApps;
    };
}
