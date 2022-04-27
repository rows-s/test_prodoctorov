import os

from .directory import DirectoryHandler
from ..report import Report

__all__ = ['FileHandler']


class FileHandler(DirectoryHandler):
    """File report handler. Inherits :class:`DirectoryHandler`."""

    def handle_report(self, report: Report) -> None :
        """Writes report into `report_name`.txt in :attr:`self.dir`"""
        report_path = self._get_path_for_report(report)
        with open(report_path, 'w+') as file:
            file.write(report.get_msg())

    def _get_path_for_report(self, report: Report) -> str:
        """returns path for the `report`"""
        return os.path.join(self.dir, report.get_report_name() + '.txt')
