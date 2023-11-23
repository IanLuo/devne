from ss.generator.deps_generator import DepsGenerator
from .fixtures import * 
from ss.configure.configure import Configure

class TestDepsGenerator:
    def test_deps_generate(self, config):
        assert DepsGenerator(Configure(config)).generate()['#DEPS#'].replace("\n", "").replace(" ", "") == ''' 
          django
          black
        '''.replace("\n", "").replace(" ", "")

