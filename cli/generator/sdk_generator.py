from ..configure.configure import Configure
from .interface.file_exporter import FileExporter
from .interface.content_generator import ContentGenerator
from functools import reduce

_TEMPLATE_FILE_PYTHON = 'templates/sdk_python.template'
_MARK_VERSION = '#VERSION#'
_MARK_PACKAGES = '#PACKAGES#'

class SdkGenerator(ContentGenerator, FileExporter):
    def __init__(self, configure: Configure):
        self.configure = configure

    def generate(self) -> str:
        # TODO:
        return '' 

    def export(self) -> str:
        return ''

    def generate_python(self, configure: Configure):
       with open(_TEMPLATE_FILE_PYTHON, 'r') as f:
           template = f.read()
           template = template.replace(_MARK_VERSION, configure.sdk_version)
           template = template.replace(_MARK_PACKAGES, self._render_packages(configure))

           return template 

    def _render_packages(self, configure: Configure):
        return reduce(lambda last, next: f'{last}\n{next}', configure.sdk_packages_dev)
