from abc import ABC
from contextlib import suppress
from dataclasses import dataclass, fields
from functools import lru_cache
from typing import Dict, Type

__all__ = ['Model']


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
        _dict = cls._migrate_camel_to_snake(_dict)  # copied inside
        for name, sub_model in cls._get_sub_models().items():
            sub_dict = _dict[name]
            _dict[name] = sub_model.from_json(sub_dict)
        return cls(**_dict)  # noqa

    @classmethod
    def _migrate_camel_to_snake(cls, _dict):
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
            with suppress(TypeError):  # suppress "clas is not a type" error
                if issubclass(_field.type, Model):
                    sub_models[_field.name] = _field.type
        return sub_models
