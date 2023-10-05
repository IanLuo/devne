from cli.dashboard import Dashboard

class TestDashboard:
    def test_list_units(self):
        env = { 'SS_UNITS': 'unit1:unit2:unit3:' }
        assert Dashboard(env).list_units() == [ 'unit1', 'unit2', 'unit3' ]
