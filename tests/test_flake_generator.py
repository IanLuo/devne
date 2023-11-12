from cli.generator.flake_metadata_generator import FlakeMetadataGenerator
from cli.generator.flake_generator import FlakeGenerator
from cli.configure.configure import Configure
from .fixtures import config

class TestFlakeGenerator:
    def test_metadata_generate(self, config):
        generator = FlakeMetadataGenerator(Configure(config))
        assert generator.generate() == {
            '#DESCRIPTION#': 'this is a project for unit test', '#NAME#': 'test project', '#VERSION#': '1.0.0'
, '#NIXPKGSREV#': 'xxxxx'
        }

    def test_flake_generator(self, config):
        generator = FlakeGenerator(Configure(config))
        assert generator.generate() == {}
