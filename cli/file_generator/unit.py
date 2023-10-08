class Unit:
    def __init__(self, json: dict, name: str) :
        if json is not None:
            for key, value in json.items():
              setattr(self, key, value)

        if name is not None:
            setattr(self, 'name', name)

    @property
    def rawJson(self):
        j = self.__dict__
        return { key: j[key] for key in j.keys() if not key.startswith('_') }

    @property
    def name(self) -> str:
        return self.rawJson['name']
