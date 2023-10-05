import json

class Unit:
    def __init__(self, **kwargs) :
        for key, value in kwargs.items():
          setattr(self, key, value)

    def to_json(self):
        json.dumps(self.__dict__)
