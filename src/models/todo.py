from dataclasses import dataclass

from .base import Model

__all__ = ['Todo']


@dataclass
class Todo(Model):
    id: int
    user_id: int
    title: str
    completed: bool

    __camel_to_snake_fields__ = {'userId': 'user_id'}
