from cli.configure.configure import Configure
from cli.configure.unit import Unit
from .fixtures import config 

class TestConfigure:
    def test_get_sdk_language(self, config):
        config = Configure(config)
        assert config.language == "python"

    def test_get_sdk_version(self, config):
        config = Configure(config)
        assert config.version == "3.8"

    def test_get_sdk_default_packages(self, config):
        config = Configure(config)
        assert config.sdkPackagesDefault == ["typer"]

    def test_get_sdk_dev_packages(self, config):
        config = Configure(config)
        assert config.sdkPackagesDev == ["pynvim"]

    def test_get_dependencies_default(self, config):
        config = Configure(config)
        assert config.dependenciesDefault == ["django"]

    def test_get_dependencies_dev(self, config):
        config = Configure(config)
        assert config.dependenciesDev == ["black"]

    def test_get_units(self, config):
        config = Configure(config)
        assert len(config.units) == 1

        unit = Unit({
            "powers.db.postgres": {
                "username": "test_user",
                "password": "test_password",
                "database": "test_database",
                "host": "",
                "folder": ""
            }
        })

        assert config.units[0].attrs == unit.attrs
        assert config.units[0].name == "powers.db.postgres"
        assert config.units[0].attrs == {
            "username": "test_user",
            "password": "test_password",
            "database": "test_database",
            "host": "",
            "folder": ""
        }
