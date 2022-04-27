from abc import ABC
from contextlib import suppress
from dataclasses import dataclass, fields
from functools import cache
from typing import TypeVar, Type, Dict

from .json import JSONSupport

_T = TypeVar('_T', bound='LazyJSON')

__all__ = ['LazyJSON']


@dataclass
class LazyJSON(JSONSupport, ABC):
    @classmethod
    def from_lazy_json(cls: Type[_T], json: dict) -> _T:
        json = json.copy()
        for snake, sub_model in cls._get_sub_models().items():
            camel = cls._get_camel(snake, default=snake)  # we store it as snake but expect camel. may be the same
            json[camel] = sub_model.from_lazy_json(json[camel])
        return cls.from_json(json)

    @classmethod
    @cache  # one cache for one class
    def _get_sub_models(cls) -> Dict[str, Type['LazyJSON']]:
        """returns sub models {`field_name`: `type`} dict. result is cached for each class"""
        sub_models = {}
        for _field in fields(cls):
            with suppress(TypeError):  # suppress "__cls is not a type" error
                if issubclass(_field.type, LazyJSON):
                    sub_models[_field.name] = _field.type
        return sub_models
