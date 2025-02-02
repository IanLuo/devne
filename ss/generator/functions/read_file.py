class ReadFile:
    def __init__(self, file_path):
        self.file_path = file_path

    def read(self):
        with open(self.file_path, 'r') as file:
            return file.read()

    # render to nix expression
    def render(self):
        return f"""
        """
