from cli.run_command import run

class TestRunner:
    def test_run_good(self):
        stdout, _ = run('echo "hello"') 
        assert stdout == 'hello\n'
      
    def test_run_bad(self):
        _, stderr = run('hello') 
        assert 'command not found' in stderr
