class NixPackage:
    value: str
    params: dict

    def __init__(self, value: str, params: dict):
        self.value = value
        self.params = params

    def render(self):
        return f"""
        """
