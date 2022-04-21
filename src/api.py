from abc import ABC
from typing import Union, List

import requests
from requests import Response

__all__ = ['API', 'MedRatingAPI']


_JSONT = Union[list, dict]


class API(ABC):
    """Abstract API class"""
    base_url = ''

    def _get(self, path) -> Response:
        return requests.get(self.base_url + path)

    def _get_json(self, path) -> _JSONT:
        return self._get(path).json()


class MedRatingAPI(API):
    """Provides methods to make api requests to MedRating"""
    base_url = 'https://json.medrating.org'
    users_path = '/users'
    todos_path = '/todos'

    def get_users(self) -> List[dict]:
        """returns list of users"""
        return self._get_json(self.users_path)

    def get_todos(self) -> List[dict]:
        """returns list of todos"""
        return self._get_json(self.todos_path)
