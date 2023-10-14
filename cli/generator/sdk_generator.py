from configure.configure import Configure
from flake_generator import FileGenerator

_TEMPLATE_FILE = 'sdk.template'

class SdkGenerator(FileGenerator):
    def __init__(self, configure: Configure):
        self.configure = configure

    def generate(self) -> str:
        # TODO:
        return '' 


