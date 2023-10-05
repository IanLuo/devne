import json

class Unit:
    def __init__(**kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
