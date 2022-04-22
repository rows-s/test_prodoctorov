from abc import ABC
from dataclasses import dataclass, field, fields
from functools import lru_cache
from contextlib import suppress

__all__ = ['Model', 'Geo', 'Address', 'Company', 'User', 'Todo']

from typing import Dict, Type


@dataclass
class Model(ABC):
    """Abstract dataclass Model that provides :meth:`from_raw_dict()`"""

    @classmethod
    def from_raw_dict(cls, _dict):
        """
        Use it if you want to create a :cls:`Model` with submodels from a whole-raw-dict
        (where submodel also represented as a dict).

        Submodels' dicts will be converted into corresponding :cls:`Model`
        """
        _dict = _dict.copy()
        for name, sub_model in cls._get_sub_models().items():
            sub_dict = _dict[name]
            _dict[name] = sub_model.from_raw_dict(sub_dict)
        return cls(**_dict)  # noqa

    @classmethod
    @lru_cache(maxsize=None)  # one cache for one class
    def _get_sub_models(cls) -> Dict[str, Type['Model']]:
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
