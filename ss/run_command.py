import subprocess
import logging


def run(command: str) -> str:
    trimmed_command = " ".join(command.strip().split())
    logging.info(f"Running command: {trimmed_command}")

    try:
        result = subprocess.run(
            trimmed_command, capture_output=True, text=True, shell=True, check=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logging.error(
            f"Command '{trimmed_command}' failed with error: {e.stderr.strip()}"
        )
        return e.stderr.strip()
