from abc import ABC
from typing import Union

import requests
from requests import Response

__all__ = ['API']

_JSON_T = Union[list, dict]


class API(ABC):
    """Abstract API class"""
    base_url = ''

    def _get(self, path) -> Response:
        return requests.get(self.base_url + path)

    def _get_json(self, path) -> _JSON_T:
        return self._get(path).json()
