from abc import ABC, abstractmethod

__all__ = ['Handler']

from ..report import Report


class Handler(ABC):
    """Basehandler class"""

    @abstractmethod
    def handle_report(self, report: Report):
        """handles report"""
