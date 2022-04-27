from typing import List

from src.apis import API

__all__ = ['MedRatingAPI']


class MedRatingAPI(API):
    """Provides methods to make api requests to MedRating"""
    base_url = 'https://json.medrating.org'
    users_path = '/users'
    todos_path = '/todos'

    def get_users(self) -> List[dict]:
        """returns list of all users"""
        return self._get_json(self.users_path)

    def get_todos(self) -> List[dict]:
        """returns list of all todos"""
        return self._get_json(self.todos_path)
