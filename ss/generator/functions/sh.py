class Sh:
    command: str
    params: dict

    def __init__(self, command: str, params: dict):
        self.command = command 
        self.params = params

    def render(self):
        return f"""
        ''
          {self.command}
        ''
        """

