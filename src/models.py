from __future__ import annotations

from abc import ABC
from dataclasses import dataclass, field, fields
from typing import Type, List, ClassVar

__all__ = ['Geo', 'Address', 'Company', 'User', 'Todo']


@dataclass
class Model(ABC):
    """Abstract dataclass Model that provides :meth:`from_raw_dict()`"""
    _sub_models: ClassVar[List[str]] = []

    @classmethod
    def __post_init__(cls):
        cls._sub_models = cls._get_sub_models_names()

    @classmethod
    def from_raw_dict(cls, _dict):
        """
        Use it if you want to create a :cls:`Model` with submodels from a whole-raw-dict
        (where submodel also represented as a dict).

        Submodels' dicts will be converted into corresponding :cls:`Model`
        """
        _dict = _dict.copy()
        for sub_model_name in cls._sub_models:
            sub_model = cls.get_field_type(sub_model_name)
            sub_dict = _dict[sub_model_name]
            _dict[sub_model_name] = sub_model.from_raw_dict(sub_dict)

        return cls(**_dict)

    @classmethod
    def _get_sub_models_names(cls) -> List[str]:
        """returns list of sub models fields' names"""
        sub_models = []
        for _field in fields(cls):
            if issubclass(_field.type, Model):
                sub_models.append(_field.name)

        return sub_models

    @classmethod
    def get_field_type(cls, name) -> Type[Model]:
        """returns type of field with given name if exists, otherwise None"""
        for _field in fields(cls):
            if _field.name == name:
                return _field.type


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
