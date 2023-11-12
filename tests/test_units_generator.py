from cli.configure.configure import Configure
from cli.generator.units_generator import UnitsGenerator
from .fixtures import * 
from cli.generator.sdk_generator import SdkGenerator

class TestUnitsGenerator:
    def test_units(self, config):
       assert UnitsGenerator(Configure(config)).generate()['#UNITS#'].replace("\n", "").replace(" ", "") == '''
       powers_db_postgres = powers.db.postgres {
           username = "test_user";
           password = "test_password";
           database = "test_database";
           host = "";
           folder = "";
         };
     '''.replace("\n", "").replace(" ", "")

    def test_units_ref(self, config):
        assert UnitsGenerator(Configure(config)).generate()['#UNITS_REF#'].replace("\n", "").replace(" ", "") == '''
        [ powers_db_postgres python ]
        '''.replace("\n", "").replace(" ", "")

    def test_sdk(self, config):
        assert UnitsGenerator(Configure(config)).generate()['#SDK#'] == SdkGenerator(Configure(config)).export()

