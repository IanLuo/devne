from cli.generator.deps_generator import DepsGenerator
from .fixtures import config
from cli.configure.configure import Configure

class TestDepsGenerator:
    def test_deps_generate(self, config):
        assert DepsGenerator(Configure(config)).generate().replace("\n", "").replace(" ", "") == ''' 
        {
          pkgs
        }:

        with pkgs; [
          django
          black
        ]
        '''.replace("\n", "").replace(" ", "")

