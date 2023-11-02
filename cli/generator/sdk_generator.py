from ..configure.configure import Configure
from .interface.file_exporter import FileExporter
from .interface.content_generator import ContentGenerator
from functools import reduce
from typing import Optional

_TEMPLATE_FILE_PYTHON = 'templates/sdk_python.template'
_MARK_VERSION = '#VERSION#'
_MARK_PACKAGES = '#PACKAGES#'
_MARK_LANGUAGE = '#LANGUAGE#'

class SdkGenerator(ContentGenerator, FileExporter):
    def __init__(self, configure: Configure):
        self.configure = configure

    def generate(self) -> dict[str, str]:
        return {
            _MARK_VERSION: self.configure.sdk_version,
            _MARK_PACKAGES: self._render_packages(self.configure),
            _MARK_LANGUAGE: self.configure.sdk_language

        }

    def export(self) -> Optional[str]:
        if self.configure.sdk_language == 'python':
            return self.export_python()

    def export_python(self):
        with open(_TEMPLATE_FILE_PYTHON, 'r') as f:
            generated = self.generate()
            template = f.read()
            template = template.replace(_MARK_VERSION, generated[_MARK_VERSION])
            template = template.replace(_MARK_PACKAGES, generated[_MARK_PACKAGES])

            return template 

    def _render_packages(self, configure: Configure):
        return '\n'.join(configure.sdk_packages_dev)
