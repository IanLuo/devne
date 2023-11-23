from ss.configure.parser import parse 
import pytest

@pytest.fixture
def yaml_configure():
    return """
        sdk:
            language: python
            version: 3.8
  """
  
class TestParser:
    def test_parse(self, yaml_configure):
        configure = parse(yaml_configure)
        assert type(configure) == type({})
