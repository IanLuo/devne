import subprocess

def run(command) -> subprocess.CompletedProcess:
  return subprocess.run(command, 
    shell=True, 
    stdout=subprocess.PIPE, 
    stderr=subprocess.PIPE, 
    universal_newlines=True)
