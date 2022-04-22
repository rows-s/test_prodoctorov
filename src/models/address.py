from dataclasses import dataclass

from .base import Model
from .geo import Geo

__all__ = ['Address']


@dataclass
class Address(Model):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo
