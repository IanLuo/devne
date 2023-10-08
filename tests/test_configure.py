from cli.configure.configure import Configure
from cli.file_generator.unit import Unit
import pytest

@pytest.fixture
def config():
    return '''
        sdk:
          language: python 
          version: "3.8"
          packages:
            default:
              - typer
            development:
              - pynvim
        
        dependencies:
          default:
            - django
          development:
            - black
        
        units:
          - postgres:
              username: "test_user"
              password: "test_password"
              database: "test_database"
              host: ""
              folder: ""
        
        # this is the official nixpkgs ref
        rev: xxxxx
    ''' 

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
        assert config.units == [Unit({
            "postgres": {
                "username": "test_user",
                "password": "test_password",
                "database": "test_database",
                "host": "",
                "folder": ""
            }
        })]

        unit = Unit({
            "postgres": {
                "username": "test_user",
                "password": "test_password",
                "database": "test_database",
                "host": "",
                "folder": ""
            }
        })

        assert unit.name == "postgres"
        assert unit.attrs == {
            "unit": "postgres",
            "username": "test_user",
            "password": "test_password",
            "database": "test_database",
            "host": "",
            "folder": ""
        }
