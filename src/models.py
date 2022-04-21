from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field, fields
from typing import Type, ClassVar, Dict

__all__ = ['Geo', 'Address', 'Company', 'User', 'Todo']


@dataclass
class Model(ABC):
    """Abstract dataclass Model that provides :meth:`from_raw_dict()`"""
    _sub_models = {}
    """{`name`: `type`}"""

    @classmethod
    def __post_init__(cls):
        cls._set_sub_models()

    @classmethod
    def from_raw_dict(cls, _dict):
        """
        Use it if you want to create a :cls:`Model` with submodels from a whole-raw-dict
        (where submodel also represented as a dict).

        Submodels' dicts will be converted into corresponding :cls:`Model`
        """
        _dict = _dict.copy()
        for name, sub_model in cls._sub_models.values():
            sub_dict = _dict[name]
            _dict[name] = sub_model.from_raw_dict(sub_dict)

        return cls(**_dict)

    @classmethod
    def _set_sub_models(cls):
        """sets cls._sub_models"""
        cls._sub_models = {}
        for _field in fields(cls):
            if issubclass(_field.type, Model):
                cls._sub_models[_field.name] = _field.type


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

    _sub_models = ('geo', )


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

    _sub_models = ('address', 'company')


@dataclass
class Todo(Model):
    id: int
    user_id: int
    title: str
    completed: bool
