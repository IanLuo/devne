{
  description = "nix flake installer for SS";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachSystem ["x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin"] (system:
      let
        pkgs = import nixpkgs { inherit system; };
        version = "0.1.0";
      in {
        packages.default = pkgs.stdenv.mkDerivation {
          pname = "ss";
          inherit version;
          src = ./.;

          nativeBuildInputs = with pkgs; [
            python312
            python312Packages.poetry
          ];

          buildInputs = with pkgs; [
            nixfmt
            jsonfmt
          ];

          # Don't run the build phase as we just need to install the Python package
          dontBuild = true;

          installPhase = ''
            mkdir -p $out/bin
            mkdir -p $out/lib

            # Copy the source files to lib directory
            cp -r ss $out/lib/

            # Create a wrapper script
            cat > $out/bin/ss << EOF
            #!${pkgs.bash}/bin/bash
            export PYTHONPATH=$out/lib:\$PYTHONPATH
            exec ${pkgs.python312}/bin/python -m ss "\$@"
            EOF

            # Make the wrapper executable
            chmod +x $out/bin/ss
          '';

          meta = with pkgs.lib; {
            description = "SS installation package";
            homepage = "https://github.com/yourusername/ss";  # Replace with actual homepage
            license = licenses.mit;  # Replace with actual license
            platforms = platforms.all;
          };
        };

        defaultPackage = self.packages.${system}.default;
      });
}
