from src.ss.configure.configure import Configure
from src.ss.folder import GEN_FOLDER, SS_FILE, UNIT_FILE, Folder
from os.path import exists
from .fixtures import *
from .test_utils import TestUtils


class TestFolder:
    def test_init_data_path(self, config):
        configure = Configure(config)
        abs_path = f"{configure.root}/{GEN_FOLDER}"
        assert exists(abs_path) == False
        assert Folder(configure.root).init_data_path() == abs_path
        assert exists(abs_path) == True

        TestUtils.clean_folders(config)

    def test_init_ss_file(self, config):
        configure = Configure(config)

        abs_path = f"{configure.root}/{SS_FILE}"
        assert exists(abs_path) == False
        assert Folder(configure.root).init_ss_file() == abs_path
        assert exists(abs_path) == True
        TestUtils.clean_folders(config)

    def test_init_unit_file(self, config):
        configure = Configure(config)

        abs_path = f"{configure.root}/{UNIT_FILE}"
        assert exists(abs_path) == False
        assert Folder(configure.root).init_unit_file() == abs_path
        assert exists(abs_path) == True
        TestUtils.clean_folders(config)
