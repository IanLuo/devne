from ss.generator.flake_metadata_generator import FlakeMetadataGenerator
from ss.generator.flake_generator import FlakeGenerator
from ss.configure.configure import Configure
from .fixtures import config

class TestFlakeGenerator:
    def test_metadata_generate(self, config):
        generator = FlakeMetadataGenerator(Configure(config))
        assert generator.generate() == {
            '#NAME#': 'test project', '#VERSION#': '1.0.0'      
        }

    def test_flake_generator(self, config):
        generator = FlakeGenerator(Configure(config))
        assert generator.generate() == {
            '#DESCRIPTION#': 'this is a project for unit test', '#NIXPKGSREV#': 'xxxxx'
        }
