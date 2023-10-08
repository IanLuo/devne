from cli.run_command import run

class TestRunner:
    def test_run_good(self):
        result = run ('echo "hello"') 
        assert result.stdout == 'hello\n'
      
    def test_run_bad(self):
        result = run ('hello') 
        assert 'command not found' in result.stderr
