import os
from datetime import datetime
from os import path

from .base import Handler
from ..report import Report

__all__ = ['FileHandler']


class FileHandler(Handler):
    """Writes reports into `report_name`.txt files in provided `directory`"""
    def __init__(self, directory: str = 'tasks'):
        self.dir = directory
        self.ensure_dir(self.dir)

    def handle_report(self, report: Report):
        """Writes report into `report_name`.txt file in `self.dir` directory"""
        report_path = path.join(self.dir, report.get_report_name() + '.txt')
        self.archive_if_exists(report_path)
        with open(report_path, 'w+') as file:
            file.write(report.get_report())

    @staticmethod
    def ensure_dir(directory: str):
        """ensures that dir exists. Create path if dir is not exists"""
        if not os.path.exists(directory):
            os.makedirs(directory)

    def archive_if_exists(self, path_):
        """rename file if exists. New name create by :meth:`_create_archive_name()`"""
        if path.exists(path_):
            os.rename(path_, self._create_archive_name(path_))

    def _create_archive_name(self, path_: str, dt_format='%d-%m-%YT%H:%M') -> str:
        """
        creates new archive name for provided `path_`.
        From 'last_name.txt' to 'old_last_name_01-01-1970T03:00.txt' where datetime is file's creation time
        """
        dir_ = path.dirname(path_)
        last_name = path.basename(path_).removesuffix('.txt')
        creation_time = self._get_creation_time(path_).strftime(dt_format)
        name = f'old_{last_name}_{creation_time}.txt'
        return path.join(dir_, name)

    @staticmethod
    def _get_creation_time(path_: str) -> datetime:
        """returns file's creation time"""
        return datetime.fromtimestamp(path.getctime(path_))
