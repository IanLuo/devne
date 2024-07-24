from dataclasses import dataclass
from typing import Dict, Any, Optional
import json
import os
from ..folder import Folder

@dataclass
class Node:
    repo: str
    rev: str
    hash: str

class Lock:
    def __init__(self, root: str):
        self.lock_path = Folder(root).lock_path

        self.load_lock()

    def find_node(self, name: str)  -> Optional[Node]:
        node = self.lock.get(name)
        if node is None:
            return None
        else:
            return Node(**node)

    def format(self):
        os.system(f'jsonfmt -w {self.lock_path}')

    def clear(self):
        self.lock = {}
        self.write_lock(self.lock)
        
    def add_node(self, name: str, node: Node) -> None:
        self.lock[name] = node.__dict__
        self.write_lock(self.lock)

    def write_lock(self, content: Dict[str, Any]) -> None:
        with open(self.lock_path, "w") as f:
            json.dump(content, f)
            
    def load_lock(self):
        if not os.path.exists(self.lock_path):
            self.lock = {}
            return

        with open(self.lock_path, "r") as f:
            self.lock = json.load(f)
