from typing import Protocol

__all__ = ['Report']


class Report(Protocol):
    """Abstract report class"""
    def get_title(self) -> str:
        """returns string that represents title"""

    def get_description(self) -> str:
        """returns string that represents description"""

    def get_report(self) -> str:
        """returns string that represents report"""
