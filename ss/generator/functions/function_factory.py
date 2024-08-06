from ss.configure.blueprint import Blueprint
from .weblink import Weblink
from .sh import Sh 
from .git_repo import GitRepo
from .nix_package import NixPackage
from ...configure.schema import *

def find_function(name: str, value: dict, params: dict, blueprint: Blueprint): 
    sh = value.get(SH)
    url = value.get(URL)
    git = value.get(GIT)

    if name == K_INSTANTIATE:    
        if sh is not None and isinstance(sh, str):
            return Sh(command=sh, params=params)
        else: 
            return None
    elif name == K_SOURCE:
        if url is not None and isinstance(url, str):
            return Weblink(value=url, params=params, blueprint=blueprint)
        elif git is not None and isinstance(git, dict):
            return GitRepo(value=git, params=params)
        else: 
            return NixPackage(value=name, params=params)

    else:
        return None
