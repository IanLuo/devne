from src.ss.generator.flake_metadata_generator import FlakeMetadataGenerator
from src.ss.generator.flake_generator import FlakeGenerator
from src.ss.configure.configure import Configure
from .fixtures import config

class TestFlakeGenerator:
    def test_metadata_generate(self, config):
        generator = FlakeMetadataGenerator(Configure(config))
        assert generator.generate() == {
            '#NAME#': 'test project', '#VERSION#': '0.0.1'      
        }

    def test_flake_generator(self, config):
        generator = FlakeGenerator(Configure(config))
        assert generator.generate() == {
            '#DESCRIPTION#': 'project description'
        }
