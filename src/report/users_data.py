from typing import Dict

from ..apis import MedRatingAPI
from ..models import User, Todo

__all__ = ['UsersData']


class UsersData:
    """class provides methods to prepare data for report"""
    _users: Dict[int, User]
    '{`user_id`: `User`}'

    def __init__(self, mr_api: MedRatingAPI):
        self._mr_api = mr_api
        self._set_users()._set_todos()

    def get_user(self, _id: int):
        return self._users.get(_id)

    def add_user(self, user: User):
        self._users[user.id] = user

    def _set_users(self):
        """returns dict {`user_id`: :cls:`User`} form MedRatingAPI"""
        self._users = {user_dict['id']: User.from_json(user_dict)
                       for user_dict in self._mr_api.get_users()}

        return self

    def _set_todos(self):
        """sets todos into corresponding users"""
        for todo_dict in self._mr_api.get_todos():
            todo = Todo.from_json(todo_dict)
            user = self.get_user(todo.user_id)
            if user is not None:
                user.todos.append(todo)

        return self

    def __iter__(self):
        return iter(self._users.values())
