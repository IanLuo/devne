import pytest
from cli.configure.configure import Configure

@pytest.fixture
def config():
    return '''
        sdk:
          language: python 
          version: "3.8"
          packages:
            default:
              - typer
            development:
              - pynvim

        dependencies:
          default:
            - django
          development:
            - black

        units:
          - powers.db.postgres:
              username: "test_user" 
              password: "test_password" 
              database: "test_database" 
              host: ""
              folder: ""
        rev: xxxxx
    '''


