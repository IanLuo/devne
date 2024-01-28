from dataclasses import dataclass
import re

@dataclass
class GitRepo:
    url: str
    rev: str
    is_matched: bool = False

    _pattern = r'^git:\/\/(.*\.git)$'

    def __init__(self, value: str):
        first_match = re.search(self._pattern, value)

        if first_match is not None:
            self.is_matched = True
            self.url = first_match.group(1)
