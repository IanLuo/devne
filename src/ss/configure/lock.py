from dataclasses import dataclass
from typing import Dict, Any, Optional
import json
import os

@dataclass
class Node:
    repo: str
    rev: str
    hash: str

class Lock:
    def __init__(self, config_path: str):
        self.lock_path = config_path + ".lock"

        self.load_lock()

    def find_node(self, name: str)  -> Optional[Node]:
        node = self.lock.get(name)
        if node is None:
            return None
        else:
            return Node(**node)

    def update_node(self, name: str, hash: str, repo: str, rev: str) -> None:
        node = self.find_node(name)
        if node is None:
            raise Exception(f"node {name} not found in lock")
        
        node.repo = repo
        node.rev = rev
        node.hash = hash
        
        self.add_node(name, node)

    def format(self):
        os.system(f'jsonfmt -w {self.lock_path}')
        
    def add_node(self, name: str, node: Node) -> None:
        self.lock[name] = node.__dict__
        self.write_lock(self.lock)

    def write_lock(self, content: Dict[str, Any]) -> None:
        with open(self.lock_path, "w") as f:
            json.dump(content, f)
            
    def remove_node(self, name: str):
        if self.find_node(name) is not None:
            del self.lock[name]
            self.write_lock(self.lock)

    def load_lock(self):
        if not os.path.exists(self.lock_path):
            self.lock = {}
            return

        with open(self.lock_path, "r") as f:
            self.lock = json.load(f)
