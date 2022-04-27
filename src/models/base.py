from abc import ABC
from dataclasses import dataclass

from .lazy_json import LazyJSON

__all__ = ['Model']


@dataclass
class Model(LazyJSON, ABC):
    """Abstract Model that provides JSON & LazyJSON supporting"""
