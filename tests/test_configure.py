from ss.configure.configure import Configure
from ss.configure.unit import Unit
from .fixtures import config 

class TestConfigure:
    def test_get_tools(self, config):
        config = Configure(config)
        assert config.tools == ["django", "black"]

    def test_name(self, config):
        config = Configure(config)
        assert config.name == "test project"

    def test_verion(self, config):
        config = Configure(config)
        assert config.version == "0.0.1"

    def test_description(self, config):
        config = Configure(config)
        assert config.description == "description for test project"

    def test_get_units(self, config):
       pass 
