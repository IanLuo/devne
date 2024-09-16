class Sh:
    def __init__(self, name: str, command: str):
        self.command = command
        self.name = name

    def render(self):
        return f"""(pkgs.writeScript \"{self.name}.sh\" ''
            #!/bin/bash
            {self.command}
            '')"""
