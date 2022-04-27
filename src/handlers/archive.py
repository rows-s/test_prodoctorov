import os
from datetime import datetime

from .file import FileHandler
from ..report import Report

__all__ = ['FileHandlerWithArchiving']


class FileHandlerWithArchiving(FileHandler):
    """File handler. Archives existing reports preventing overwriting"""
    def handle_report(self, report: Report) -> None:
        """Archives existing report file before save new one."""
        path_ = self._get_path_for_report(report)
        if os.path.exists(path_):
            self.archive_report(path_)
        super().handle_report(report)

    def archive_report(self, path_: str) -> None:
        """renames report"""
        os.rename(path_, self._create_archive_path(path_))

    def _create_archive_path(self, path_: str, dt_format: str = '%d-%m-%YT%H:%M') -> str:
        """
        creates new archive name for provided `path_`.
        Template: 'old_{last_name}_{creation_time}.txt'
        """
        dir_ = os.path.dirname(path_)
        last_name = os.path.basename(path_).removesuffix('.txt')
        creation_time = self._get_c_time(path_).strftime(dt_format)
        name = f'old_{last_name}_{creation_time}.txt'
        return os.path.join(dir_, name)

    @staticmethod
    def _get_c_time(path_: str) -> datetime:
        """returns file's creation time"""
        return datetime.fromtimestamp(os.path.getctime(path_))
