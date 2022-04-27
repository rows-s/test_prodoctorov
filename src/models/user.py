from dataclasses import dataclass, field
from typing import List

from .todo import Todo
from .base import Model
from .company import Company
from .address import Address

__all__ = ['User']


@dataclass
class User(Model):
    id: int
    name: str
    username: str
    email: str
    phone: str
    website: str
    address: Address
    company: Company
    todos: List[Todo] = field(default_factory=list, init=False)

    def add_todo(self, todo: Todo):
        self.todos.append(todo)
