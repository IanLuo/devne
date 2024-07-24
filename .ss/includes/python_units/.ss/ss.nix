
        { pkgs ? import <nixpkgs> {} }:
        let
        ss = pkgs.importFlake /nix/store/8szshk2rwyzvzmhwk2i4ykq4ckjd4zgj-templates-f997706/flake.nix {};
nixpkgs = pkgs.callPackage /nix/store/na2zx8q48fjvprwrl359sdhv0cyaanv8-nixpkgs-7c67f72/default.nix {};
        name = "python_units";
        version = "1.0";
        units = pkgs.callPackage ./unit.nix { inherit ss nixpkgs; };
        in
        pkgs.mkShell {
            name = name;
            version = version;
            buildInputs = [
                units
            ];

            shellHook = ''
                echo "Welcome to ${name} shell"
                ${units.scripts}
            '';
        }
        