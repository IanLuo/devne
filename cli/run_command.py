import subprocess
from rich import print

def run(command): 
    process = subprocess.Popen(command, 
      shell=True, 
      stdout=subprocess.PIPE, 
      stderr=subprocess.PIPE, 
      universal_newlines=True)

    stdout, stderr = process.communicate()

    if stdout != None:
        print(f"[yellow]{stdout}[/yellow]") 

    if stderr != None:
      print(f"[bold red]{stderr}[/bold red]")
