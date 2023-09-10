from cli.configure.parser import parse 

class TestParser:
    def test_parse(self):
        configure = {}
        parse(configure)
        assert configure == {}
