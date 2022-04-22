from typing import Dict

from ..apis import MedRatingAPI
from ..models import User, Todo

__all__ = ['UsersData']


class UsersData:
    """class provides methods to prepare data for report"""
    _users: Dict[str, User]

    def __init__(self, mr_api: MedRatingAPI):
        self._mr_api = mr_api
        self._set_users()._set_todos()

    def _set_users(self):
        """returns dict {`user_id`: :cls:`User`} form MedRatingAPI"""
        self.users = {user_dict['id']: User.from_json(user_dict)
                       for user_dict in self._mr_api.get_users()}
        return self

    def _set_todos(self):
        """sets todos into corresponding users"""
        for todo_dict in self._mr_api.get_todos():
            user = self._users.get(todo_dict.get('userId'))
            if user is not None:
                user.todos.append(Todo.from_json(todo_dict))
        return self


