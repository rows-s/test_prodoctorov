from abc import ABC, abstractmethod

__all__ = ['Stream']


class Stream(ABC):
    """Abstract stream"""
    @abstractmethod
    def __init__(self):
        pass
