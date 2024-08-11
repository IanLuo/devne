- Control work cycle
  start work, end work
  commit code
  portato clock
  staging status
  code summary
- Resource center
  In charge of the folder and paths for each generated file
- A thin wrapper over nix shell scripts, let nix developer easy to hack
  The tool will only try to [generate](file_generator.md) or complementary the flake.nix, and use the current nix machanism

  The flake.nix file will only generate for the first time, so user can directly modify it, there are other override and imports
  which used by devne used, user can not change, they will be 'hidden' in the devne folder, and devne cli will activatly modify them.

```
ss
  up
  reload
  update [name]
  actions 
    list
    exec
  dashboard
``t`
