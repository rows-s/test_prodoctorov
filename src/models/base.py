from abc import ABC
from contextlib import suppress
from dataclasses import dataclass, fields
from functools import lru_cache
from typing import Dict, Type

__all__ = ['Model']


@dataclass
class Model(ABC):
    """Abstract dataclass Model that provides :meth:`from_lazy_json()`"""
    __camel_to_snake_fields__ = {}

    @classmethod
    def from_lazy_json(cls, json):
        """
        Use it if you want to create a :cls:`Model` with submodels from a whole-raw-dict
        (where submodel also represented as a `dict`).

        Submodel's dict will be converted into corresponding :cls:`Model`
        """
        json = cls._migrate_camel_to_snake(json)  # copied inside
        for name, sub_model in cls._get_sub_models().items():
            json[name] = sub_model.from_lazy_json(json[name])
        return cls(**json)  # noqa

    @classmethod
    def _migrate_camel_to_snake(cls, _dict):
        """
        changes all `_dict`'s keys that are represented in `cls.__camel_to_snake_fields__ to according values.
        returns new :cls:`dict`
        """
        _dict = _dict.copy()
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
            with suppress(TypeError):  # suppress "__cls is not a type" error
                if issubclass(_field.type, Model):
                    sub_models[_field.name] = _field.type
        return sub_models
