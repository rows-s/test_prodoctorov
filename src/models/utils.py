from contextlib import suppress
from typing import Type

from . import Model

__all__ = ['ensure_from_json']


def ensure_from_json(model: Type[Model], json: dict, default=None):
    """Trying to create instance of `model` from json. If any Exception is raised returns None, otherwise instance"""
    with suppress(Exception):
        return model.from_json(json)
    return default
