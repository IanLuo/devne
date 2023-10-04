ROOT_FOLDER = 'ss/'
CONFIG_FILE =f"{ROOT_FOLDER}/ss.yaml"
FLAKE_FILE = f'{ROOT_FOLDER}/flake.nix'
DATA_FOLDER = f'{ROOT_FOLDER}/data'

from os.path import exists 
from os import makedirs

class Folder:
    def getDataPath(name, create = False) -> str:
        path = f"{DATA_FOLDER}/{name}"
        if exists(path) == False and create:
            mkdirs(path)

        return path 
