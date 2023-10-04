import os
from typing import List

class Dashboard:
    def __init__(self, env: dict):
        self.env = env

    def listUnits(self) -> List[str]:
        return [ unit for unit in self.env.get('SS_UNITS').split(':') if unit != '' ]

if __name__ == '__main__':
    d = Dashboard(os.environ)
    print(d.listUnits())
