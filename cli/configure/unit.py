from typing import Optional

_KEY_NAME = 'unit'

class Unit:
    def __init__(self, json: Optional[dict] = None, name: Optional[str]  = None) :
        '''
        json: a json representation of the object
        name: the name of the Unit
        '''
        if json is not None:
            if len(json.keys()) != 1:
                raise ValueError("malformed configure, should have 1 and only 1 top leve key as the name of unit")

            name = list(json.keys())[0]
            setattr(self, _KEY_NAME, name)

            for key, value in json[name].items():
                setattr(self, key, value)

        if name is not None:
            setattr(self, _KEY_NAME, name)

    @property
    def attrs(self):
        '''Return a json representation of the object'''
        j = self.__dict__
        return { key: j[key] for key in j.keys() if not key.startswith('_') and key != _KEY_NAME }

    @property
    def name(self) -> str:
        '''Return the name of the Unit'''
        return self.__dict__['unit']

    def __eq__(self, other):
        return self.attrs == other.attrs
