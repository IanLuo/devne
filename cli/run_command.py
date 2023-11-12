import subprocess
from rich import print
from typing import Tuple

def run(command: str) -> Tuple[str, str]: 
    process = subprocess.Popen(command, 
      shell=True, 
      stdout=subprocess.PIPE, 
      stderr=subprocess.PIPE, 
      universal_newlines=True)

    stdout, stderr = process.communicate()

    if stdout != None:
        print(f"[green]{stdout}[/green]") 

    if stderr != None:
      print(f"[bold orange]{stderr}[/bold orange]")

    return stdout, stderr
