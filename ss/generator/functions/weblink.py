from ss.configure.blueprint import Blueprint
import hashlib
import re

class Weblink:
    name: str
    value: str
    params: dict
    blueprint: Blueprint

    def __init__(self, value: str, params: dict, blueprint: Blueprint):
        self.value = self.replace_vars(value=value, params=params)
        self.params = params
        self.blueprint = blueprint

    def replace_vars(self, value: str, params: dict) -> str:
        pattern = r'\$([a-zA-Z0-9_]+)'
        return re.sub(pattern, lambda x: str(params.get(x.group(1), x.group(0))), value)

    def render(self):
        name = self.make_name(self.value)
        locked_node = self.blueprint.resource_manager.lock.find_node(name)

        if locked_node is None:
            hash = self.blueprint.resource_manager.nix_resource_manager.fetch_for_url(self.value)
            if not bool(hash):
                raise Exception(f"no hash found for {self.value}")
            self.blueprint.resource_manager.lock.add_new(name=name, repo=self.value, hash=hash, rev='')
        else:
            hash = locked_node.hash

        return f"""
            builtins.fetchurl {{
              url = "{self.value}";
              sha256 = "{hash}";
            }}
        """

    @classmethod
    def make_name(cls, url: str) -> str:
        return hashlib.md5(url.encode()).hexdigest()



