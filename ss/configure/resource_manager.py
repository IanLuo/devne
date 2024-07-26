import json 
from typing import Optional, Dict
import re
import logging
from ..run_command import run
from .lock import Lock, Node
from dataclasses import dataclass
from ..folder import Folder

@dataclass
class Resource:
    local_path: str
    rev: str
    remote_path: str
    hash: str
    locked: bool

class ResourceManager:
    def __init__(self, lock_root: str, config_folder: Folder):
        self.lock = Lock(lock_root)
        self.config_folder = config_folder
        self.nix_resource_manager = NixResourceManager(config_folder=config_folder)

    def fetch_resource(self, name: str, value: Dict) -> Resource:
        node = self.lock.find_node(name)
        if node is not None:
            logging.info(f"node found for {name}: {node}")
            hash = node.hash 
            rev = node.rev
            url = node.repo
            local_path = self.nix_resource_manager.get_store_path_from_git(url=url, hash=hash, rev=rev)
            return Resource(local_path=local_path, rev=rev, remote_path=url, hash=hash, locked=True)
        else:
            logging.info(f"node is not found found for {name}")
            resource = self.nix_resource_manager.fetch_resource(name, value)

            if resource.locked:
                new_node = Node(rev=resource.rev, repo=resource.remote_path, hash=resource.hash or '')
                self.lock.add_node(name, new_node)

            return resource

class NixResourceManager:
    def __init__(self, config_folder: Folder):
        self.config_folder = config_folder

    def fetch_resource(self, name: str, value: Dict) -> Resource:
        url = value.get("url")
        if url is None:
            raise Exception(f"no url found for resource {name}")

        if url.startswith('path:'):
            store_path = self.fetch_for_path(path=self.resolve_path(url=url, folder=self.config_folder))
            hash = '' 
            rev = ''
            locked = False
        else:
            rev = value.get('rev') or self.get_commit(url, value.get('ref'))
            hash = self.fetch_for_git(url=url, rev=rev)
            store_path = self.get_store_path_from_git(url=url, hash=hash, rev=rev)
            locked = True 

        logging.info(f"command result: {store_path}")

        pattern = r'(/nix/store/[^"]+)'
        match = re.search(pattern, store_path)

        if match:
            matched = match.group(1) 
            logging.info(f"resource fetched to {matched}")
        else:
            raise Exception(f'failed to fetch resource from {url}')

        return Resource(local_path=matched, rev=rev, remote_path=url, hash=hash, locked=locked)

    def resolve_path(self, url: str, folder: Folder):
        if url.startswith('path:///.'):
            return url.replace('.', folder.path)
        else:
            return url

    def get_store_path_from_git(self, url, hash, rev):
        cmd = f'''nix-store -r \
            $(nix-instantiate -E \
                \"with import <nixpkgs> {{}}; \
                    (fetchgit {{ url = \\"{url}\\"; \
                    sha256 = \\"{hash}\\"; \
                    rev = \\"{rev}\\"; }})\")'''
        local_path = run(cmd)
        logging.info(f"store path: {local_path}")
        return local_path

    def get_commit(self, url: str, ref: Optional[str]) -> str:
        if ref is None:
            get_commit = f'git ls-remote {url} HEAD ref/heads | awk \'/\\tHEAD$/ {{print $1}}\''
        else:
            get_commit = f'git ls-remote {url} {ref} | awk \'{{print $1}}\''

        logging.info('fetching rev..')
        rev = run(get_commit)
        if len(rev) == 0:
            raise Exception(f"failed to get commit for {url}")
        logging.info(f'using rev {rev} for {url}')
        if rev is None:
            raise Exception(f"failed to get commit for {url}")

        return rev 

    def fetch_for_path(self, path) -> str:
        command = f'nix-instantiate --eval --json -E "fetchTree {path}"'

        if command is None:
            raise Exception("fail to get store path for {url}")

        store_path = run(command)
        return store_path


    def fetch_for_url(self, url: str) -> str:
        hash = run(f'nix-prefetch-url {url}')

        logging.info(f"hash for url [{url}]: {hash}")

        return hash 


    def fetch_for_git(self, url: str, rev: str) -> str:
        result = run(f'nix-prefetch-git --url {url} --rev {rev}') 

        hash = json.loads(result).get('sha256')

        logging.info(f"hash for git [{url}]: {hash}")
        return hash 
