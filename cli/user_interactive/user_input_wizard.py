from typing import Optional

class InputItem:
    def __init__(self, title: str, is_optional: bool):
        self._title = title
        self._value = None
        self._is_optional = is_optional

    @property
    def is_optional(self) -> bool:
        return self._is_optional

    @property
    def title(self) -> str:
        return self._title

    @property
    def value(self) -> Optional[str]:
        return self._value

    @value.setter
    def value(self, value: str):
        self._value = value

class UserInputWizard:
    def __init__(self, input_items: list[InputItem]):
        self._input_items = input_items

    def run(self) -> dict:
        print("Please enter the following values:")
        for item in self._input_items:
            if item.is_optional:
                item.value = input(f'{item.title} (optional): ')
            else:
                item.value = input(f'{item.title}: ')

        if not self.confirm():
            self.run()

        return { item.title: item.value for item in self._input_items }

    def validate(self, value) -> bool:
        if value == None:
            return False

        return True

    def confirm(self):
        print("Please confirm the following values:")
        for item in self._input_items:
            print(f'{item.title}: {item.value}')

        return input('Confirm? (y/n): ') == 'y'

    
