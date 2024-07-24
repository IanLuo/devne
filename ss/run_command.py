import subprocess
import logging

def run(command: str) -> str: 
    trim = lambda x: " ".join(x.replace('\n', '').replace('\r', '').split())
    command = trim(command)
    logging.info(f"running command: {command}")

    result = subprocess.run(command, 
                            capture_output=True,
                            text=True,
                            shell=True
                           )

    try:
        result.check_returncode()
    except subprocess.CalledProcessError as e:
        raise e

    output = result.stdout.strip()
    return output
