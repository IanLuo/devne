# SS

In software development, people are dealing with different requirements, working on different projects with different technologies and programming languages, and follow different daily routines to keep the work going well, they all rely on some tools or pattern, and using them every day.

## The problem

1. Seup up a development environment is time consuming, __Nix__ is greate tool to fix that, only it a little hard to learn, and most people don't like to spend the effort.
2. There are a lot of good resources out there, tools and code pieces, or text base resources, just hard to make use of them in your project, so people tend to reinvent the wheels again and again, not knowing those are already exisited at all, it's such a wate. It it great to have them at your hand.
3. There are many fix action routines we developers will follow everyday, but different for each project, or company, it will be very nice to be able to define and share across them for a group that use them.

### To fix 1

SS build on top of __Nix__, shares the idea of reproducability environment, and to make it simple, there's no new language to learn, just use __YAML__ to declarative write done what is used for the project, the dependencies, the configurations, etc.

### To fix 2

While the environment can be simplify define with a __YAML__, there's more can be defined. Because __Nix__ is such a good dependenciy manager, it contains a huge number of resources, and also able to customized it, SS can define tool and make use of any resource, or programs, and create new ones with them, and also composable. So you can use the tools create by others directly.

### To fix 3

SS also have this __Action__ system to combine all the tools together, working as a building block of pipeline, to flexibly make customized working process, and also sharable with the project source, everything are reproduciable.

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

## Flow of Actions

Action flow is also defined in 'actions', only value is a list. when that action fires, it will execute each action one by one, with some pretty good features:
The latter action with got result of the prevouse as parameter
Actions in action flow can be an action, or another action flow

```yaml

actions:
  test-flow1:
      - sh>: echo $1
      - sh>: |
            echo "result form step1: $1"
      - sh>: |
            echo "result form step2: $1"
      - action>: actions.test-flow2
      - sh>: |
            echo "result form step4: $1"
```

Actions and Action flows can work together, an action flows can have one step referent to another action flow, this give the action great power to compose other tools and make unique and reuseable functionalities.
