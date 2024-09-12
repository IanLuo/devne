class Python:
  def __init__(self, name: str, command: str):
    self.name = name
    self.command = command

  def render(self):
    return f"""(pkgs.writeScript \"{self.name}.py\" ''
            #! /bin/env python3
            {self.command}
            '')"""
