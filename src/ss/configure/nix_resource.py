import os
from typing import Optional, Dict
import re
import logging
from ..run_command import run
from .lock import Lock, Node

class NixResource:
    def __init__(self, lock: Lock):
        self.lock = lock

    # handle include
    def find_flake_to_import(self, store_path: str) -> Optional[str]:
        flake_path = os.path.join(store_path, "flake.nix")

        if os.path.exists(flake_path):
            return flake_path
        else:
            return None

    def find_ss_to_import(self, store_path: str) -> Optional[str]:
        ss_path = os.path.join(store_path, "ss.yaml")

        if os.path.exists(ss_path):
            return ss_path

        return None

    def fetch_resource(self, name: str, value: Dict) -> str:
        url = value.get("url")
        if url is None:
            raise Exception(f"no url found for resource {name}")

        result = self.fetch_for_url(name, url, value.get("branch"), value.get("rev"))

        logging.info(f"command result: {result}")

        pattern = r'(/nix/store/[^"]+)'
        match = re.search(pattern, result)

        if match:
            matched = match.group(1) 
            logging.info(f"resource fetched to {matched}")
            return matched
        else:
            raise Exception(f'failed to fetch resource from {url}')

    def fetch_for_url(self, name: str, url: str, branch: Optional[str], rev: Optional[str]) -> str:
        if url.startswith("path://"):
            command = f'nix-instantiate --eval --json -E "fetchTree {url}"'

            if command is None:
                raise Exception("fail to get store path for {url}")

            store_path = run(command)
        else:
            node = self.lock.find_node(name)
            rev = rev or 'HEAD' 
            get_commit = f'git ls-remote {url} {rev} | awk \'/\\tHEAD$/ {{print $1}}\''
            branch = branch or 'nil'
            def store_path_cmd(url, hash, rev):
                return f'''nix-store -r \
                    $(nix-instantiate -E \
                        \"with import <nixpkgs> {{}}; \
                            (fetchgit {{ url = \\"{url}\\"; \
                            sha256 = \\"{hash}\\"; \
                            branchName = \\"{branch}\\"; \
                            rev = \\"{rev}\\"; }})\")'''

            if node is not None:
                logging.info(f"node found for {name}")
                hash = node.hash 
                rev = node.rev
                url = node.repo
                store_path = run(store_path_cmd(url, hash, rev))
            else:
                logging.info(f"node not found for {name}")
                logging.info('fetching rev..')
                rev = run(get_commit)
                if len(rev) == 0:
                    raise Exception(f"failed to get commit for {url}")
                logging.info(f'using rev {rev} for {url}')
                if rev is None:
                    raise Exception(f"failed to get commit for {url}")
                hash = run(f'nix-prefetch-url --unpack {url}/archive/{rev}.tar.gz') 
                store_path = run(store_path_cmd(url, hash, rev))

                self.lock.add_node(name, Node(url, rev, hash))


        logging.info(f"store_path for url {store_path}")
        
        return store_path 
