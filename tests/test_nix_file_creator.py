from cli.generator.nix_files_creator import NixFilesCreator
from cli.configure.configure import Configure
from .fixtures import *
from .test_utils import TestUtils 

class TestNixFileExportor:
    def test_export(self, config):
        file_creator = NixFilesCreator(Configure(config))
        assert file_creator.create() == True
        TestUtils.clean_folders(config)


