from cli.configure.configure import Configure

class TestConfigure:
    def test_init(self):
        config = {}
        c = Configure(config)
        assert c.config == config
    
    def test_begin(self):
        config = {}
        c = Configure(config)
        c.begin()
        assert c.config == config
    
    def test_finish(self):
        config = {}
        c = Configure(config)
        c.finish()
        assert c.config == config
