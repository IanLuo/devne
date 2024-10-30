class Doc:
    def __init__(self, content):
        self.content = content

    def render(self):
        return f"""
          pkgs.writeText "doc" ''
            {self.content}
          ''
    """
