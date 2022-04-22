from functools import partial
from contextlib import suppress

from . import Model, User, Todo

__all__ = ['try_from_json', 'try_user_from_json', 'try_todo_from_json']


def try_from_json(model: Model, json: dict, default=None):
    """Trying to create instance of `model` from json. If any Exception is raised returns None, otherwise instance"""
    with suppress(Exception):
        return model.from_json(json)
    return default


try_user_from_json = partial(try_from_json, User)
try_todo_from_json = partial(try_from_json, Todo)
