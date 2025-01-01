{ pkgs, lib, ... }: let system = builtins.currentSystem; in { inherit system; }
