from src.ss.configure.configure import Configure
from src.ss.configure.unit import Unit
from .fixtures import config
from src.ss.configure.functions.git_repo import GitRepo

class TestConfigure:
    def test_source(self, config):
        config = Configure(config)
        assert config.sources['units'].name == 'units'
        assert config.sources['units'].value == 'latest'

    def test_metadata(self, config):
        config = Configure(config)
        assert config.metadata.name == 'test project'
        assert config.metadata.version == '0.0.1'
        assert config.metadata.description == 'project description'

    def test_resolve_vars(self, config):
        config = Configure(config)
        assert config.dict['units']['another']['db'] == config.dict['units']['db_postgres']

    def test_resolve_function(self, config):
        config = Configure(config)
        assert isinstance(config.dict['units']['source_from_git'], GitRepo)
    def test_resolve_units(self, config):
        config = Configure(config)
        assert len(config.all_unit_instances) == 4
        assert len(config.units_for_source('units')) == 3
        assert len(config.units_for_source('pkgs')) == 1
        assert len(config.units_for_source('other')) == 0
        assert config.unit_from_source('units', 'db_postgres') != None
        assert config.unit_from_source('units', 'db_postgres').definition.attrs['username'] == 'test'
        assert isinstance(config.unit_from_source('units', 'source_from_git').definition.attrs, GitRepo)
        assert config.unit_from_source('units', 'another').definition.attrs['db']['database'] == 'database'


