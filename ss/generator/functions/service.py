class Service:
    def __init__(self, name: str, value: dict):
        self.name = name
        self.value = value

    def render(self):
        return self.value
