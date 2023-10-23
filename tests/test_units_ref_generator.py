from cli.generator.units_ref_generator import UnitsRefGenerator
from .fixtures import config
from cli.configure.configure import Configure
import unittest

class TestUnitsRefGenerator:
    """Tests for `units_ref_generator.py`."""

    def test_generate(self, config):
        """Test something."""
        self.units_ref_generator = UnitsRefGenerator(Configure(config))
        assert self.units_ref_generator.generate() == '[ powers.db.postgres ]'
