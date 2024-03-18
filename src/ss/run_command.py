import subprocess
import threading

def run(command: str): 
    def stdout_printer(p):
        for line in p.stdout:
            print(line.rstrip())

    p = subprocess.Popen(command, stdin=subprocess.PIPE, 
                         shell=True,
                         stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         universal_newlines=True)

    t = threading.Thread(target=stdout_printer, args=(p,))
    t.start()

    p.stdin.write((command + "\n")) if p.stdin is not None else None
    p.stdin.flush() if p.stdin is not None else None

    p.stdin.close() if p.stdin is not None else None
    t.join()
