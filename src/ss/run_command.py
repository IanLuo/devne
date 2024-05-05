import subprocess
from typing import Optional

def run(command: str) -> Optional[str]: 
    result = subprocess.run(command, 
                            capture_output=True,
                            text=True,
                            shell=True
                           )
    output = result.stdout.strip()
    return output
