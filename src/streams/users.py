from typing import Dict, Type, Iterator

from .base import Stream
from ..apis import MedRatingAPI
from ..models import Todo, User
from ..models.utils import ensure_from_lazy_json

__all__ = ['UsersStream']


class UsersStream(Stream):
    """class provides methods to prepare data for report"""

    def __init__(self, mr_api: MedRatingAPI, user_cls: Type[User] = User):
        self._mr_api: MedRatingAPI = mr_api
        self._users: Dict[int, User] = {}
        self._user_cls: Type[User] = user_cls

        self._set_users()._set_todos()

    def get_user(self, id_: int):
        """returns :class:`User` with provided :var:`id_`"""
        return self._users.get(id_)

    def add_user(self, user: User):
        """adds :var:`user` to the stream"""
        self._users[user.id] = user

    def _set_users(self):
        """sets self._users dict form MedRatingAPI"""
        for user_json in self._mr_api.get_users():
            user = ensure_from_lazy_json(self._user_cls, user_json)
            if user is None:
                continue
            self.add_user(user)

        return self

    def _set_todos(self):
        """sets todos into corresponding users"""
        for todo_json in self._mr_api.get_todos():
            todo = ensure_from_lazy_json(Todo, todo_json)
            if todo is None:
                continue

            user = self.get_user(todo.user_id)
            if user is not None:
                user.add_todo(todo)

        return self

    def __iter__(self) -> Iterator[User]:
        return iter(self._users.values())
