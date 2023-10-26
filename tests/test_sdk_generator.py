from cli.generator.sdk_generator import SdkGenerator
from cli.configure.configure import Configure

class TestSdkGenerator:
    def __init__(self, configure: Configure):
        self.generator = SdkGenerator(configure)

    def test_generate_sdk_python(self):
        pass
