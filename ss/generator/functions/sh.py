class Sh:
    def __init__(self, name: str, content: str | dict):
        if isinstance(content, dict):
            if len(content) != 1:
                raise ValueError("sh> must contain only one key")
            self.command = list(content.values())[0]
            self.name = f"{name}-{list(content.keys())[0]}"
        else:
            self.command = content
            self.name = name

    def render(self):
        return f"""(pkgs.writeScript \"{self.name}.sh\" ''
            #!/bin/bash
            {self.command}
            '')"""
