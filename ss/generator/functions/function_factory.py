from .weblink import Weblink
from .sh import Sh 
from .git_repo import GitRepo
from .nix_package import NixPackage

SH = 'sh>'
URL = 'url>'
GIT = 'git>'
READFILE = 'read_file>'
K_SOURCE = 'source'
K_INSTANTIATE = 'instantiate'
K_ACTIONS = 'actions'

def find_function(name: str, value: dict): 
    keys_to_remove_as_parms = [K_SOURCE, K_INSTANTIATE, K_ACTIONS]
    params = {k: v for k, v in value if k not in keys_to_remove_as_parms}
    sh = value.get(SH)
    url = value.get(URL)
    git = value.get(GIT)

    if name == K_INSTANTIATE:    
        if sh is not None and isinstance(str, sh):
            return Sh(command=sh, params=params)
        else: 
            return None
    elif name == K_SOURCE:
        if url is not None and isinstance(str, url):
            return Weblink(value=url, params=params)
        elif git is not None and isinstance(dict, git):
            return GitRepo(value=git, params=params)
        else: 
            return NixPackage(value=name, params=params)

    else:
        return None
