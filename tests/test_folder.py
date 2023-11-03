from cli.configure.configure import Configure
from cli.folder import DATA_FOLDER, FLAKE_FILE, UNIT_FILE, CONFIG_FILE, Folder 
from os.path import exists
from .fixtures import *
from .test_utils import TestUtils 

class TestFolder:
    def test_init_data_path(self, config):
        configure = Configure(config)
        abs_path = f'{configure.root}/{DATA_FOLDER}'
        assert exists(abs_path) == False 
        assert Folder(configure.root).init_data_path() == abs_path
        assert exists(abs_path) == True

        TestUtils.clean_folders(config)

    def test_init_flake_file(self, config):
        configure = Configure(config)

        abs_path = f'{configure.root}/{FLAKE_FILE}'
        assert exists(abs_path) == False
        assert Folder(configure.root).init_flake_file() == abs_path
        assert exists(abs_path) == True
        TestUtils.clean_folders(config)

    def test_init_unit_file(self, config):
        configure = Configure(config)

        abs_path = f'{configure.root}/{UNIT_FILE}'
        assert exists(abs_path) == False
        assert Folder(configure.root).init_unit_file() == abs_path
        assert exists(abs_path) == True
        TestUtils.clean_folders(config)

    def test_config_file(self, config):
        configure = Configure(config)

        abs_path = f'{configure.root}/{CONFIG_FILE}'
        assert exists(abs_path) == False
        assert Folder(configure.root).init_config_file() == abs_path
        assert exists(abs_path) == True
        TestUtils.clean_folders(config)
