from typing import Optional
from dataclasses import dataclass

@dataclass
class Unit:
    name: str
    attrs: dict

    def __init__(self, json: Optional[dict] = None, name: Optional[str]  = None) :
        '''
        represents a ss template functional unit, which can be used as parameter to another unit
        '''
        if json is not None:
            if len(json.keys()) != 1:
                raise ValueError("malformed configure, should have 1 and only 1 top leve key as the name of unit")

            name = list(json.keys())[0]
            self.name = name
            self.attrs = json[name]

        if name is not None:
            self.name = name

