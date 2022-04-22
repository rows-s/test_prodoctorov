from dataclasses import dataclass

from .base import Model

__all__ = ['Geo']


@dataclass
class Geo(Model):
    lat: str
    lng: str
