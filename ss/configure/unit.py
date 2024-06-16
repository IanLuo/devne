from typing import Optional
from dataclasses import dataclass


@dataclass
class Unit:
    name: str
    attrs: Optional[dict]

    def __init__(self, name: str, params: Optional[dict[str, dict]] = None):
        self.name = name
        self.attrs = params
