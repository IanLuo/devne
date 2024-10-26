class Sh:
    def __init__(self, name: str, content: str):
        self.command = content
        self.name = name

    def render(self):
        return f"""(pkgs.writeScript \"{self.name}.sh\" ''
            #!/bin/bash
            {self.command}
            '')"""
