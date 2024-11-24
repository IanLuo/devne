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

## Project

The working environment is called a project, represented as a ss.yaml file, you can define everything you needed to control and share you environment, tools, actions and routines in it, and only this file, other projects can also be included into your project to make use of theirs predefined configurations.

## Units

A unit is a basic source of function provider, it contains something that can help you with your job, like some software, some resource, or scripts that can be used by other units.

```yaml
python:
    source: python_units.python
    version: "3.12.0"
```

This is a simple unit, it adds python 3.12.0 to your working environment.

Notice that the source is come from /python_units/, which is another project we included, if we check the definition from \python_units/, there's something more interesting:

```yaml
python:
    version: "3.10.0"
    doc: |
      *version* is the version of python to use.
      *instantiate* is the command to create a virtual environment, and automatically activate when the working
      environment is entered.
    source: nixpkgs-python.packages.${sslib.env.system}.${version}
    onstart:
      sh>: |
        python -m venv .venv${version}
        source .venv${version}/bin/activate
```

Let's explain it line by line:

`version: "3.10.0"`: This is a parameter, that can be overwriten, in our example is it over write with '3.12.0' by passing a new value at where it is referenced.

`doc: xxxx`: This is to provide documentation for this unit, if you are making your own unit, here is where you add the documentation with markdown.

`source`: If a unit needs some resource to work with, in this case *python* requires to install *python*, with the specified version, so this is how it is added. There'a are a bunch of other ways to added source, and source can be anything.

`onstart`: This is a special item, items inside *onstart* can be any actionable content, and will be ran when your environment starts up. In this case we want a venv to be activate once the environment starts, so this is how to make this happen.

When using this unit, just like the code above, we create an unit in sour project *ss.yaml* file, and put the source as the one you want:

```yaml
python:
    source: python_units.python
    version: "3.12.0"
```

Now we created a new *python* unit, extending the one from project *python_units*, and with different version of python, while other properties, like the scripted *onstart* and *documentation*, is passed down and will available directly.

## Action

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

When the value of an action is a list of actionable items, it will execute each action one by one, with some pretty good features:
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

Actions can reference to any other ss.yaml from other sources, and directly use them as they were defined locally, or customize it with parameters, if it declared any:

```yaml
git-helper:
    source: templates.git-helper
    ignores: ["result", ".direnv", ".ss", ".venv*", ".pytest_cache", ".mypy_cache", "dist", "build", "*.egg-info", ".tox", ".nox", ".coverage", ".eggs", "__pycache__", ".pytest"]
```

## Services

Services only live in the project level, not under any unit, the difference of service is that, a service is keep running in the background, action is executed when triggered.

## Trigger

Trigger can be time schedule, or callback of other action
