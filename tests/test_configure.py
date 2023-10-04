from cli.configure.configure import Configure
import pytest

@pytest.fixture
def config():
  return {
    "language": "python",
    "version": "3.8",
  }

class TestConfigure:
  '''
  Start working
  1. Enable dev environment (with nix)
  2. Triger dashboard 
  '''
  def test_begin(self, config):
    pass
  
  def test_finish(self, config):
    pass

  def test_get_language(self, config):
    config = Configure(config)
    assert config.language == "python3.8"

  def test_get_server_missing(self, config):
    c = Configure(config)
    assert c.server == None 

  def test_get_server(self, config):
    config["server"] = "builtin"
    c = Configure(config)
    assert c.server == 'builtin' 
