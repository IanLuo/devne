# WIP
[ ] import other ss.yaml and generate files for them
[ ] units can be observed

# BACKLOG
[ ] unit documentations
[ ] command auto completion
[ ] welcome information
[ ] ss.yaml validation
[ ] ss.yaml helper, used in website
[ ] local shared store
[ ] support services, like database, redis, thrid party services, inside
    docker

# ARCHIVE
[x] to make unit runnable
    add doc for each unit, by adding a special parameter 'doc', by default null
    to specify input/output type for each unit
[x] add sha-256 for ss.yaml include so download could be cached
[x] units have executable interface
[x] yaml file will extend other yaml files to 'inherit' the existing tools and packgage setups
[x] in a yaml, the name should be customized and referenced
[x] to customize yaml will be only thing to do, work with script that can be referenced from yaml file to control other actions
[x]!! support outside unit
[x] ref from outside repo on github
[x] resolve vars
[x] resolve funcitons
  [x] git repo
[x]collect units
[x]!! versioning for packages in yaml
[x] reconstruct configure to define all logic with yaml, including package fetching, action definition, environment setup, combining etc
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
