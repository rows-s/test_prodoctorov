from abc import ABC
from dataclasses import dataclass, field, fields
from functools import lru_cache
from contextlib import suppress

__all__ = ['Model', 'Geo', 'Address', 'Company', 'User', 'Todo']

from typing import Dict, Type


@dataclass
class Model(ABC):
    """Abstract dataclass Model that provides :meth:`from_json()`"""
    __camel_to_snake_fields__ = {}

    @classmethod
    def from_json(cls, _dict):
        """
        Use it if you want to create a :cls:`Model` with submodels from a whole-raw-dict
        (where submodel also represented as a `dict`).

        Submodel's dict will be converted into corresponding :cls:`Model`
        """
        _dict = _dict.copy()
        _dict = cls._migrate_camel_to_snake(_dict)
        for name, sub_model in cls._get_sub_models().items():
            sub_dict = _dict[name]
            _dict[name] = sub_model.from_json(sub_dict)
        return cls(**_dict)  # noqa

    @classmethod
    def _migrate_camel_to_snake(cls, _dict):
        for last_name, new_name in cls.__camel_to_snake_fields__.items():
            if last_name in _dict:
                _dict[new_name] = _dict.pop(last_name)
        return _dict

    @classmethod
    @lru_cache(maxsize=None)  # one cache for one class
    def _get_sub_models(cls) -> Dict[str, Type['Model']]:
        """returns sub models dict with struct {`field_name`: `type`}. result is cached for each class"""
        sub_models = {}
        for _field in fields(cls):
            with suppress(TypeError):  # suppress "clas is not a type" error
                if issubclass(_field.type, Model):
                    sub_models[_field.name] = _field.type
        return sub_models


@dataclass
class Geo(Model):
    lat: str
    lng: str


@dataclass
class Address(Model):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo


@dataclass
class Company(Model):
    name: str
    catch_phrase: str
    bs: str

    __camel_to_snake_fields__ = {'catchPhrase': 'catch_phrase'}


@dataclass
class User(Model):
    id: int
    name: str
    username: str
    email: str
    phone: str
    website: str
    address: Address
    company: Company
    todos: list = field(default_factory=list)


@dataclass
class Todo(Model):
    id: int
    user_id: int
    title: str
    completed: bool

    __camel_to_snake_fields__ = {'userId': 'user_id'}
