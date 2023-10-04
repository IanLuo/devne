from cli.dashboard import Dashboard

class TestDashboard:
    def testListUnits(self):
        env = { 'SS_UNITS': 'unit1:unit2:unit3:' }
        assert Dashboard(env).listUnits() == [ 'unit1', 'unit2', 'unit3' ]
