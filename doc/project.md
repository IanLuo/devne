After running the devne command, a `flake.nix` file will be generated, only for the first time, and later the command 
will only update some small parts in it, they should be only used for composing tools, like git, database, 
project management etc.

Advanced users and manually update this file as long as they don't modify the parts maitained by devne cli.

[x] How to organize the base `flake.nix` and components?
    - User `overlays`?
    - Or just `callPackage`?
use callPackage directly


```
.ss
  ss.nix
  units.nix
  /inclues
    /python_units
      ss.nix
      units.nix
```
