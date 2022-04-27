from abc import ABC, abstractmethod

__all__ = ['Report']


class Report(ABC):
    """Abstract report class"""
    @abstractmethod
    def get_report_name(self):
        """returns name for the report"""

    @abstractmethod
    def get_title(self) -> str:
        """returns string that represents title"""

    @abstractmethod
    def get_description(self) -> str:
        """returns string that represents description"""

    @abstractmethod
    def get_msg(self) -> str:
        """returns string that represents report"""
