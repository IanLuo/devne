from configure.configure import Configure
from flake_generator import FileGenerator

class DepsGenerator(FileGenerator):
    def __init__(self, configure: Configure):
        self.configure = configure

    def generate(self) -> str:
        # TODO:
        return ''
