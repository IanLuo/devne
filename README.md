# Client commands

[ CLI ] (cli/cli.md)

# Env configure sharing

- Choose and apply env
- Upload and manage personal env configure
- Configure file search
- Integrate tools

# Env configure edit

- Generate Flake.nix from configure files
  - Format and protocol to express the configuration

  # Traditional process

  ## To make a development environment reproduciable

  1.
  Write
  down
  tools
  needed, probably versions

2. Write down how to setup up and init those tools
3. Write down how to prepare environment and initial data
4. Write down how to start to project

## To setup new env on a new machine

1. Clone the project locally
2. According to the document, do everything one by one, this might take a while
3. Try to run the project, if not working, back to step `2`

## When initializing a new project

1. Install and setup dependencies
2. Create folers and files
3. Run the skeleton for the first time

## The power comes from integration of everything

All units can be used together as a pipeline, and to generate a result,
by defining a chain of units

## Actions

From the name action, is to perform a specific activity, it is compbined with a unit, and can use the resource of that unit.
For example, we can make use the [git-extras](https://github.com/tj/git-extras), by wrape it as a unit, and provide some actions to it:

```yaml
units:
  git-helper:
      source: nixpkgs.git-extras
      actions:
        summary:
          sh>: git summary --line
```

Above is definition of a unit calls *git-helper*, which use the project *git-extras* which already on nixpkgs, in fact most of tools we can simple get in this way, *nixpkgs* is a huge source of dependencies. When we specified the source, git-extra will be available in our environment, along with it's all commands, we can directly use it, or create a action to call a script that using it, just as the *summary* above.

Actions are not simple a alias to call bash commands, you can write any script as you want, as long as the envrionment can access it, and to access it, you only need to add a unit to use it.

Actions are bulding blocks for other actions, and actions-flows, once defined, you can refer to it in other actons, or action-flows, and the on-start script, which is realy handle when you want to re-use your handy tools, especially when you have many.

```yaml
poetry:
    source: nixpkgs.poetry
    actions:
      install:
        sh>: poetry install
      add:
        sh>: poetry add $1
      list:
        sh>: poetry list
      build:
        sh>: poetry build

```

## Action-flows

Action-flow is a sequece of actions, it execute each action one by one, with some pretty good features:
The latter action with got result of the prevouse as parameter
Actions in action flow can be an action, or another action flow

```yaml

test-flow1:
    - sh>: echo $1
    - sh>: |
          echo "result form step1: $1"
    - sh>: |
          echo "result form step2: $1"
    - action-flow>: ss.actions-flows.test-flow2
    - sh>: |
          echo "result form step4: $1"
```

Actions and Action-flows can both be defined on unit as well as on project, and they both use the key *Actions* and *Action-flows*, they works in the same way, just for different usage and re-use size, to put them in deferrent level, on units they are more focus on the specific unit, while on project they are more like work across units, or not unit dependented.
