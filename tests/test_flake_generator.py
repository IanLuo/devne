from cli.generator.flake_generator import FlakeGenerator
from cli.configure.configure import Configure
from .fixtures import config

class TestFlakeGenerator:
    def test_generate(self, config):
        generator = FlakeGenerator(Configure(config))
        assert generator.generate() == {
            '#DESCRIPTION#': 'this is a project for unit test', '#NAME#': 'test project', '#VERSION#': '1.0.0'
        }
