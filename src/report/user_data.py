from typing import Dict

from ..apis import MedRatingAPI
from ..models import User, Todo

__all__ = ['UserData']


class UserData:
    """class provides methods to prepare data for report"""
    def __init__(self, mr_api: MedRatingAPI):
        self._mr_api = mr_api
        self.users = self._get_users()
        self._set_todos()

    def _get_users(self) -> Dict[str, User]:
        """returns dict {`user_id`: :cls:`User`} form MedRatingAPI"""
        return {user_dict['id']: User.from_json(user_dict)
                for user_dict in self._mr_api.get_users()}

    def _set_todos(self):
        """sets todos into corresponding users"""
        for todo_dict in self._mr_api.get_todos():
            user = self.users.get(todo_dict.get('userId'))
            if user is not None:
                user.todos.append(Todo.from_json(todo_dict))


