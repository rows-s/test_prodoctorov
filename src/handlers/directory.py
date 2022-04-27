import os
from abc import ABC

from .base import Handler

__all__ = ['DirectoryHandler']


class DirectoryHandler(Handler, ABC):
    """Abstract Directory handler. Stores `directory`. Ensures that the path exists"""
    def __init__(self, directory: str):
        self.dir: str = directory
        self.ensure_dir(self.dir)

    @staticmethod
    def ensure_dir(directory: str):
        """ensures that dir exists. Create path if dir not exists"""
        if not os.path.exists(directory):
            os.makedirs(directory)
