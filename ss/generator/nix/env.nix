{ pkgs, ... }: let system = builtins.currentSystem; in { inherit system; }
