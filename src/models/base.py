from abc import ABC
from dataclasses import dataclass

from .lazy_json import LazyJSONModel

__all__ = ['Model']


@dataclass
class Model(LazyJSONModel, ABC):
    """Abstract Model that provides JSON & LazyJSON supporting"""
