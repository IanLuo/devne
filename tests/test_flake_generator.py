from cli.generator.flake_generator import FlakeGenerator
from cli.configure.configure import Configure
import pytest

@pytest.fixture
def configure():
    return Configure('''

    ''')

class TestFlakeGenerator:
    def test_generate(self, configure):
        assert FlakeGenerator(configure).generate() is not None
