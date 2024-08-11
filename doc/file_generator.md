# New project
# Integrate current project

# generate from configure file
    Every time there's anything changed in ss.yaml, fellow nix files will be re-generated

```
ss.yaml -> ss.nix + units.nix

```

ss.nix: The main nix configure file

units.nix: units mentioned in ss.yaml, only existed in sstemplate, which are some convenient nix modules that 
can help user with common functions that might be useful.

includes folder: all units referenced, which can be:
- default.nix
- ss.yaml
- flake.nix
ss.yaml will be generated to a pare of ss.nix and units.nix, others will be directly usable, those references are accessable in your ss.yaml, you can defien units with them directly
