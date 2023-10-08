import os
from typing import List

class Dashboard:
    def __init__(self, env: dict):
        self.env = env

    def list_units(self) -> List[str]:
        return [ unit for unit in self.env['SS_UNITS'].split(':') if unit != '' ]

if __name__ == '__main__':
    d = Dashboard(dict(os.environ))
    print(d.list_units())
