from ss.configure.configure import Configure
from ss.configure.unit import Unit
from .fixtures import config 

class TestConfigure:
    def test_get_sdk_language(self, config):
        config = Configure(config)
        assert config.sdk_language == "python"

    def test_get_sdk_version(self, config):
        config = Configure(config)
        assert config.sdk_version == "3.8"

    def test_get_sdk_default_packages(self, config):
        config = Configure(config)
        assert config.sdk_packages_default == ["typer"]

    def test_get_sdk_dev_packages(self, config):
        config = Configure(config)
        assert config.sdk_packages_dev == ["pynvim", "pillow"]

    def test_get_tools(self, config):
        config = Configure(config)
        assert config.tools == ["django", "black"]

    def test_name(self, config):
        config = Configure(config)
        assert config.name == "test project"

    def test_verion(self, config):
        config = Configure(config)
        assert config.version == "1.0.0"

    def test_description(self, config):
        config = Configure(config)
        assert config.description == "this is a project for unit test"

    def test_get_units(self, config):
        config = Configure(config)
        units = config.units or []
        assert len(units or []) == 1

        unit = Unit({
            "powers.db.postgres": {
                "username": "test_user",
                "password": "test_password",
                "database": "test_database",
                "host": "",
                "folder": ""
            }
        })

        assert units[0].attrs == unit.attrs
        assert units[0].name == "powers.db.postgres"
        assert units[0].attrs == {
            "username": "test_user",
            "password": "test_password",
            "database": "test_database",
            "host": "",
            "folder": ""
        }
