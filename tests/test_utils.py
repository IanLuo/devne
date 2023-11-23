from os.path import exists 
from shutil import rmtree
from os import chmod, remove
from ss.folder import ROOT_FOLDER, CONFIG_FILE
import stat
from ss.configure.configure import Configure

class TestUtils:
    @staticmethod
    def clean_folders(config: str):
        configure = Configure(config)
        data_path = f'{configure.root}/{ROOT_FOLDER}'
        if exists(data_path):
            chmod(data_path, stat.S_IRWXU)
            rmtree(data_path)

        config_path = f'{configure.root}/{CONFIG_FILE}'
        if exists(config_path):
            chmod(config_path, stat.S_IRWXU)
            remove(config_path)
