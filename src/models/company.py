from dataclasses import dataclass

from .base import Model


__all__ = ['Company']


@dataclass
class Company(Model):
    name: str
    catch_phrase: str
    bs: str

    __camel_to_snake_fields__ = {'catchPhrase': 'catch_phrase'}
