import pytest
from os import path

@pytest.fixture
def config():
    return path.join(path.dirname(__file__), 'test.yaml')


