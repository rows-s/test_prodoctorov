from typing import Iterator

from .users import UsersStream
from ..apis import MedRatingAPI
from ..report import UserReport

__all__ = ['UserReportsStream']


class UserReportsStream(UsersStream):
    def __init__(self, mr_api: MedRatingAPI, *args, **kwargs):
        super().__init__(mr_api, user_cls=UserReport)

    def __iter__(self) -> Iterator[UserReport]:
        """returns :class:`UserReport` iterator"""
        return super().__iter__()  # noqa
