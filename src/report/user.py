from dataclasses import dataclass, field
from datetime import datetime
from typing import List, ClassVar

from .base import Report
from ..models import User, Todo

__all__ = ['UserReport']


@dataclass
class UserReport(User, Report):
    """class provides methods for prepare user report"""
    done_todos: List[Todo] = field(default_factory=list, init=False)
    undone_todos: List[Todo] = field(default_factory=list, init=False)
    dt_format: ClassVar[str] = '%d.%m.%Y %H:%M'

    @property
    def title(self):
        return f'Отчёт для {self.company.name}.'

    @property
    def description(self):
        t_now = datetime.now()
        desc = f'{self.name} <{self.email}> {t_now.strftime(self.dt_format)}\n'
        desc += f'Всего задач: {len(self.todos)}\n'
        return desc

    def add_todo(self, todo: Todo):
        super().add_todo(todo)
        if todo.completed:
            self.done_todos.append(todo)
        else:
            self.undone_todos.append(todo)

    def _get_done_todos_detail(self):
        return f'Завершённые ' + self._get_todos_detail(self.done_todos) + '\n'

    def _get_undone_todos_detail(self):
        return f'Оставшиеся ' + self._get_todos_detail(self.undone_todos) + '\n'

    @staticmethod
    def _get_todos_detail(todos: List[Todo]):
        def cut_title(todo: Todo, limit=48, fill_with='...'):
            return todo.title[:limit] + (fill_with if len(todo.title) > 48 else '')

        return f'задачи: ({len(todos)})\n' + '\n'.join(map(cut_title, todos))

    def get_report(self):
        return '\n'.join((self.title, self.description, self._get_done_todos_detail(), self._get_undone_todos_detail()))
