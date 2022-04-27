from dataclasses import dataclass, field
from datetime import datetime
from typing import List, ClassVar, Generator, Iterable

from .base import Report
from ..models import User, Todo

__all__ = ['UserReport']


@dataclass
class UserReport(User, Report):
    """class provides methods for prepare user's state for report"""

    @property
    def done_todos(self) -> List[Todo]:
        """list of todos where `_todo.completed` is True"""
        return [todo for todo in self.todos if todo.completed]

    @property
    def undone_todos(self) -> List[Todo]:
        """list of todos where `_todo.completed` is False"""
        return [todo for todo in self.todos if not todo.completed]

    def get_report_name(self):
        """returns `self.username`"""
        return self.username

    def get_title(self):
        """returns template: 'Отчёт для {self.company.name}.'"""
        return f'Отчёт для {self.company.name}.'

    def get_description(self, dt_format: str = '%d.%m.%Y %H:%M'):
        """
        returns template:
            {self.name} <{self.email}> {dt_now}\n
            Всего задач: {len(self.todos)}\n
        """
        dt_now = datetime.now().strftime(dt_format)
        desc = f'{self.name} <{self.email}> {dt_now}\n'
        desc += f'Всего задач: {len(self.todos)}\n'
        return desc

    def get_done_todos_detail(self):
        return f'Завершённые ' + self._get_todos_detail(self.done_todos) + '\n'

    def get_undone_todos_detail(self):
        return f'Оставшиеся ' + self._get_todos_detail(self.undone_todos) + '\n'

    @staticmethod
    def _get_todos_detail(todos: List[Todo]):
        """
        returns string that according to template:
            задачи ({len_of_todos}):\n
            {todos_titles}
        where titles separated by newline and each is cut down to 48 characters, tail replaced with "..."
        """
        def cut_title(todo: Todo, limit=48, fill_with='...'):
            return todo.title[:limit] + (fill_with if len(todo.title) > 48 else '')

        titles_detail = '\n'.join(map(cut_title, todos))
        return f'задачи: ({len(todos)})\n' + titles_detail

    def get_msg(self, sep: str = '\n'):
        """
        returns title, description. done_todos_detail & un_done_todos_detail if they exist.
        All separated with new line
        """
        report_parts = [self.get_title(), self.get_description()]
        if self.done_todos:
            report_parts.append(self.get_done_todos_detail())
        if self.undone_todos:
            report_parts.append(self.get_undone_todos_detail())
        return sep.join(report_parts)
