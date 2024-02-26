from typing import Optional
from dataclasses import dataclass

@dataclass
class Unit:
    name: str
    attrs: dict

    def __init__(self, name: str  = None, params: Optional[dict[str, dict]] = None) :
        self.name = name
        self.attrs = params

