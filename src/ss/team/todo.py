from enum import Enum

class TodoPriority(Enum):
    LOW = 0
    MEDIUM = 1
    HIGH = 2

class TodoCategory(Enum):
    BACKLOG = "backlog"
    ARCHIVED = "archived"
    WIP = "wip"

class TodoItem:


    def __init__(self, title: str,
                 is_checked: bool = False,
                 prioerity: TodoPriority = TodoPriority.LOW,
                 catetory: TodoCategory = TodoCategory.BACKLOG):
        self._title = title 
        self._is_checked = is_checked
        self._prioerity = prioerity 
        self._catetory = catetory

    @property
    def is_checked(self) -> bool:
        return self._is_checked

    @property
    def title(self) -> str:
        return self._title

    @property
    def catetory(self) -> TodoCategory:
        return self._catetory

    @property
    def prioerity(self) -> TodoPriority:
        return self._prioerity

