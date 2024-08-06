from typing import Optional 

class GitRepo:
    url: str
    ref: Optional[str]
    rev: Optional[str]
    lock_root: str
    params: Optional[dict]

    def __init__(self, value: dict, params: Optional[dict]):
        self.params = params

        url = str(value.get("url"))
        if url is None:
            raise Exception("url is required for GitRepo")
        else:
            self.url = url

        self.rev = value.get("rev")
        self.ref = value.get("ref")

    def render(self):
        return f"""
            builtints.fetchGit {{
              url = {self.url};
              {'' if self.rev == None else f'{self.rev};'}
              {'' if self.ref == None else f'{self.ref};'}
            }}
            """
