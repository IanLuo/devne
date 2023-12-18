from typing import Optional
from rich import print
import typer
from dataclasses import dataclass

@dataclass
class InputItem:
    is_optional: bool
    title: str
    value: Optional[str] = None

class UserInputWizard:
    def __init__(self, input_items: list[InputItem]):
        self._input_items = input_items

    def run(self) -> dict:
        print("Please enter the following values:")
        step = 0
        while step < len(self._input_items):
            item = self._input_items[step]
            label = f'{item.title}{": (optional)" if item.is_optional else ""}'
            value = typer.prompt(f'{label}')

            if self._validate(value):
                item.value = value
                step += 1
            else:
                print(f'please enter a valid value for \'{item.title}\'')

        if not self._confirm():
            self.run()

        return { item.title: item.value for item in self._input_items }

    def _validate(self, value) -> bool:
        if value == '':
            return False

        return True

    def _confirm(self):
        print("---------")

        for item in self._input_items:
            print(f'{item.title}: [bold]{item.value}[/bold]')

        return input('Confirm? (y/n): ') == 'y'

    
