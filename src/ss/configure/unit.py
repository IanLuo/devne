from typing import Optional
from dataclasses import dataclass 
import re
import json as j

@dataclass
class Unit:
    name: str
    attrs: dict 

    def __init__(self, json: Optional[dict[str, dict]] = None, name: Optional[str]  = None) :
        '''
        represents a ss template functional unit, which can be used as parameter to another unit
        '''

        unit_pattern = r'^\<(.*)\>$'
        if json is not None:
            def _mapAttrs(tuple) -> tuple:
                key, value = tuple
                
                if isinstance(value, str):
                    first_match = re.search(unit_pattern, value)

                    if first_match is not None:
                        name = key.replace('.', '_')
                        value = first_match.group(1)
                        return (name, Unit(name=value))
                    else: 
                        return (key, value)
                elif isinstance(value, dict):
                    if len(value.keys()) == 1 and re.search(unit_pattern, j.dumps(value)) != None:
                        return (key, Unit(json=value))
                    else:
                        return (key, value)
                else:
                    return (key, value)
                
            if len(json.keys()) != 1:
                raise ValueError("malformated configure, should have 1 and only 1 top leve key as the name of unit")

            self.name = str(list(json.keys())[0])

            values = json[self.name]
            if not isinstance(values, dict):
                raise ValueError("malformated configure, unit value should be a dict")

            self.attrs = dict(map(_mapAttrs, values.items()))

        if name is not None:
            self.name = name
            self.attrs = {}

