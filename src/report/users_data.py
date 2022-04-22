from typing import Dict

from ..apis import MedRatingAPI
from ..models import Todo
from ..models.utils import ensure_from_json
from .user import UserReport

__all__ = ['UsersData']


class UsersData:
    """class provides methods to prepare data for report"""
    _users: Dict[int, UserReport]
    '{`user_id`: `User`}'

    def __init__(self, mr_api: MedRatingAPI):
        self._mr_api = mr_api
        self._users = {}

        self._user_cls = UserReport
        self._set_users()._set_todos()

    def get_user(self, _id: int):
        return self._users.get(_id)

    def add_user(self, user: UserReport):
        self._users[user.id] = user

    def _set_users(self):
        """sets self._users dict form MedRatingAPI"""
        for user_json in self._mr_api.get_users():
            user = ensure_from_json(UserReport, user_json)
            if user is None:
                continue
            self.add_user(user)

        return self

    def _set_todos(self):
        """sets todos into corresponding users"""
        for todo_json in self._mr_api.get_todos():
            todo = ensure_from_json(Todo, todo_json)
            if todo is None:
                continue

            user = self.get_user(todo.user_id)
            if user is not None:
                user.add_todo(todo)

        return self

    def __iter__(self):
        return iter(self._users.values())
