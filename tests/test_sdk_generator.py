from cli.generator.sdk_generator import SdkGenerator
from cli.configure.configure import Configure
from .fixtures import config

class TestSdkGenerator:
    def test_generate_sdk_python(self, config):
        self.generator = SdkGenerator(Configure(config))
        assert self.generator.generate()['#LANGUAGE#'] == 'python'
        assert self.generator.generate()['#VERSION#'] == '3.8'
        assert self.generator.generate()['#PACKAGES#'] == 'typer pynvim pillow'
