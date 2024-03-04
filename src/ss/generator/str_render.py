class StrRender:
    def __init__(self, render_str: str):
        self.render_str = render_str

    @property
    def render(self) -> str:
        return self.render_str
