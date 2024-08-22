class Sh:
    command: str
    params: dict

    def __init__(self, name: str, command: str, params: dict):
        self.command = command 
        self.params = params
        self.name = name

    def render(self):
        return f"""(pkgs.writeScript \"{self.name}.sh\" ''
            #! /bin/env bash
            {self.command}
            '')"""

