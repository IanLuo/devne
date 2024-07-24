
        { pkgs ? import <nixpkgs> {} }:
        let
        nixpkgs = pkgs.callPackage /nix/store/nribqsvvlfsj7424mgz0y0ax9d0xz6mj-nixpkgs-453402b/default.nix {};
        name = "ss-templates";
        version = "None";
        units = pkgs.callPackage ./unit.nix { inherit nixpkgs; };
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
        