from dataclasses import dataclass
from typing import Optional

@dataclass
class GitRepo:
    url: str
    ref: Optional[str]
    rev: Optional[str]

    @staticmethod
    def is_git_repo(value: dict):
        return value.get('git') is not None

    def __init__(self, value: dict):
        url = value.get('url')
        if url is None:
            raise Exception("url is required for GitRepo")
        self.rev = value.get('rev')
        self.ref = value.get('ref')

    def __str__(self):
        return f'''
builtints.fetchGit {{ 
url = {self.url}; 
rev = {self.rev}; 
ref = {self.ref}; 
}}
'''
