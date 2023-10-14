from cli.configure.configure import Configure
from cli.generator.units_generator import UnitsGenerator
from .fixtures import config

class TestUnitsGenerator:
    def testSDK(self, config):
        assert UnitsGenerator(Configure(config)).generate() == '''
            sdk = sdk {
                name="sdk";
                version="1.0.0";
            } 
        '''
