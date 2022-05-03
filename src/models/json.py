from abc import ABC
from dataclasses import dataclass
from functools import cache
from typing import Type, TypeVar

__all__ = ['JSONModel']

_T = TypeVar('_T', bound='JSONModel')


@dataclass
class JSONModel(ABC):
    __camel_to_snake_fields__ = {}

    @classmethod
    @property
    @cache  # one cache for one class
    def __snake_to_camel_fields__(cls) -> dict:
        return {v: k for k, v in cls.__camel_to_snake_fields__.items()}

    @classmethod
    def from_json(cls: Type[_T], json: dict) -> _T:
        """creates instance from provided json. Keys are migrated from camel to snake naming"""
        json = cls._migrate_to_snake(json.copy())
        return cls(**json)  # noqa

    @classmethod
    def _migrate_to_snake(cls, json: dict) -> dict:
        """
        changes all `dict_`'s keys that are represented in `cls.__camel_to_snake_fields__ to according values.
        returns new :class:`dict`
        """
        for camel in cls.__camel_to_snake_fields__:
            cls._migrate_field(camel, cls._get_snake(camel), json=json)
        return json

    @classmethod
    def _get_snake(cls, camel: str, default=None):
        return cls.__camel_to_snake_fields__.get(camel, default)

    @classmethod
    def _migrate_to_camel(cls, json: dict):
        for snake in cls.__snake_to_camel_fields__:  # noqa: PyCharm thinks it's a property instance
            cls._migrate_field(snake, cls._get_camel(snake), json=json)
        return json

    @classmethod
    def _get_camel(cls, snake: str, default=None):
        return cls.__snake_to_camel_fields__.get(snake, default)  # noqa

    @staticmethod
    def _migrate_field(last_key: str, new_key: str, json: dict):
        if last_key in json:
            json[new_key] = json.pop(last_key)
