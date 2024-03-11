# WIP

[ ]!! support outside unit
  [ ] ref from outside repo on github
  [x] resolve vars
  [x] resolve funcitons
    [x] git repo
  [x]collect units

# BACKLOG

[ ]!! interface for define hash for each unit
[ ]!! install and use in another project
[ ]!! binary package
[ ]!! ruby env and package
[ ]! python web env and package
[ ]! AI project env and package
[ ] update flake description and nixpkgsrev when flake.nix exists
[ ] unit documentations
[ ] command auto completion
[ ] check github flows for inspiration
[ ] welcome information
[ ]! package search function
[ ]! unit search function
[ ] ss.yaml validation
[ ] ss.yaml helper, used in website
[ ] units guide
[ ] ss.yaml package rev option
[ ] local shared store
[ ] to make unit runnable
    add doc for each unit, by adding a special parameter 'doc', by default null
    to specify input/output type for each unit
[ ] support services, like database, redis, thrid party services, inside
    docker

# ARCHIVE

[x]! option to show version number
[x]!! put inputs to passthrus so other units can reuse
[x]!! ss.yaml unit ref
[x]!! make write unit simple
[x]!! simplify ss.yaml
[x] setup env and packagage: default, test, docker (add more if needed)
[x] setup cli project structure, including src and tests
[x] setup tests
[x] define unit
[x] read unit list
[x] start envrionment
[x] use defineUnit function to define python, pytest and postgres
[x] add Typer and basic usage
[x] generate supporting file for units: manage path and folders, generated files
[x] folder structure and path manage for units
[x] user input wizard
[x] read pkgsrev from remote conf
[x] command in app to start to env
[x] make file generator work correctly, and use the generated flake.nix for development
[x] remote global configure
[x] commnads structure
[x] postgres database function
[x] move ss.yaml metadata into another reloadable nix file, instead of put inside flake.nix, so ss.yaml reload will take effect always
[x] package native python application
