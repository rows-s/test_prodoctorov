from typing import Dict

from api import MedRatingAPI
from models import User, Todo


class ReportData:
    """class provides methods to prepare data for report"""
    def __init__(self, mr_api: MedRatingAPI):
        self._mr_api = mr_api
        self.users = self.get_users()
        self.set_todos()

    def get_users(self) -> Dict[str, User]:
        """returns dict {`user_id`: :cls:`User`} form MedRatingAPI"""
        return {user_dict['id']: User.from_json(user_dict)
                for user_dict in self._mr_api.get_users()}

    def set_todos(self):
        """sets todos into corresponding users"""
        for todo_dict in self._mr_api.get_todos():
            user = self.users.get(todo_dict.get('userId'))
            if user is not None:
                user.todos.append(Todo.from_json(todo_dict))


def main():
    report_data = ReportData(mr_api=MedRatingAPI())
    for user in report_data.users.values():
        print(user.id, user.todos)


if __name__ == '__main__':
    main()

