from typing import Dict

from api import MedRatingAPI
from models import User


class ReportData:
    def __init__(self, mr_api: MedRatingAPI):
        self.mr_api = mr_api
        self.users = self.get_users()
        self.set_todos()

    def get_users(self) -> Dict[str, User]:
        """returns dict {`user_id`: :cls:`User`}"""
        return {user_dict['id']: User.from_raw_dict(user_dict)
                for user_dict in self.mr_api.get_users()}

    def set_todos(self):
        """sets todos into users"""
        for todo in self.mr_api.get_todos():
            user = self.users.get(todo.get('userId'))
            if user is not None:
                user.todos.append(todo)

