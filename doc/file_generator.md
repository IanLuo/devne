# New project
# Integrate current project

# generate from configure file
    Every time there's anything changed in ss.yaml, fellow(all nix files except the first version of flake.nix)
    nix files will be re-generated

```
ss.yaml -> [flake.nix] + units.nix + deps.nix

```

flake.nix: The main flake configure file, will be used by nix, with a `flake.lock` file generated and managed by 
nix, we will generate the first version of this file, then later version will only keep other nix files 
sync with ss.yaml, flake.nix is a tempalte file anyway, but experienced user can directly modify `flake.nix` to
add whatever function they want

units.nix: units mentioned in ss.yaml, only existed in sstemplate, which are some convenient nix modules that 
can help user with common functions that might be useful.

dpes.nix: dependencies that are not managed by sdk
