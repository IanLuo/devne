from cli.generator.nix_files_exportor import NixFilesExportor
from cli.configure.configure import Configure
from .fixtures import config

class TestNixFileExportor:
    def test_export(self, config):
        exportor = NixFilesExportor(Configure(config))
        pass

