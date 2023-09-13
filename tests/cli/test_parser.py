from cli.configure.parser import parse 
import pytest

@pytest.fixture
def yaml_configure():
  return """
    language: python
    version: 3.8
    server: builtin
  """
  
class TestParser:
  def test_parse(self):
    configure = {}
    parse(configure)
    assert configure == {}
