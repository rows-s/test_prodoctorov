import os
from dataclasses import dataclass, field
import itertools
from datetime import datetime
from typing import List, Generator, Iterable

import requests


@dataclass
class Todo:
    id: int
    user_id: int
    title: str
    completed: bool


@dataclass
class User:
    id: int
    name: str
    username: str
    email: str
    company_name: str
    done_todos: List[Todo] = field(default_factory=list, init=False)
    undone_todos: List[Todo] = field(default_factory=list, init=False)

    @property
    def todos(self) -> Generator[Todo, None, None]:
        for todo in itertools.chain(self.done_todos, self.undone_todos):
            yield todo

    def add_todo(self, todo: Todo):
        if todo.completed:
            self.done_todos.append(todo)
        else:
            self.undone_todos.append(todo)


def get_users(url: str = 'https://json.medrating.org/users') -> Generator[User, None, None]:
    for json in requests.get(url).json():
        yield User(id=json['id'], name=json['name'], username=json['username'],
                   email=json['email'], company_name=json['company']['name'])


def get_todos(url: str = 'https://json.medrating.org/todos') -> Generator[Todo, None, None]:
    for json in requests.get(url).json():
        if 'userId' not in json:
            continue
        json['user_id'] = json.pop('userId')
        yield Todo(**json)


def ensure_dir(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)


def archive(path: str) -> None:
    if os.path.exists(path):
        os.rename(path, create_archive_path(path))


def create_archive_path(path_: str, *, dt_format: str = '%d-%m-%YT%H:%M') -> str:
    dir_ = os.path.dirname(path_)
    last_name = os.path.basename(path_).removesuffix('.txt')
    creation_time = get_c_time(path_).strftime(dt_format)
    name = f'old_{last_name}_{creation_time}.txt'
    return os.path.join(dir_, name)


def get_c_time(path_: str) -> datetime:
    return datetime.fromtimestamp(os.path.getctime(path_))


def save_user_report(report: str, *, path: str) -> None:
    with open(path, 'w+') as file:
        file.write(report)


def create_user_report(user: User, dt_format: str = '%d.%m.%Y %H:%M') -> str:
    dt_now = datetime.now().strftime(dt_format)

    report_msg = f'Отчёт для {user.company_name}\n' \
                 f'{user.name} <{user.email}> {dt_now}\n' \
                 f'Всего задач: {len(user.done_todos) + len(user.undone_todos)}\n'

    if user.done_todos:
        report_msg += '\n' + create_todos_report('Завершённые', user.done_todos)

    if user.undone_todos:
        report_msg += '\n' + create_todos_report('Оставшиеся', user.undone_todos)

    return report_msg


def create_todos_report(name: str, todos: List[Todo]) -> str:
    titles = (todo.title for todo in todos)
    return f'{name} задачи ({len(todos)})\n' + get_titles_detail(titles) + '\n'


def get_titles_detail(titles: Iterable[str]) -> str:
    def reduce_title(title: str, limit=48, tail_replacement='...') -> str:
        return title[:limit] + (tail_replacement if len(title) > limit else '')

    return '\n'.join(map(reduce_title, titles))


def main(directory: str) -> None:
    ensure_dir(directory)
    users: dict[int, User] = {user.id: user for user in get_users()}

    for todo in get_todos():
        users[todo.user_id].add_todo(todo)

    for user in users.values():
        path = os.path.join(directory, user.username + '.txt')
        if os.path.exists(path):
            archive(path)

        save_user_report(create_user_report(user), path=path)


if __name__ == '__main__':
    main(directory='tasks')
