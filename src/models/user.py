from dataclasses import dataclass, field

from .base import Model
from .company import Company
from .address import Address

__all__ = ['User']


@dataclass
class User(Model):
    id: int
    name: str
    username: str
    email: str
    phone: str
    website: str
    address: Address
    company: Company
    todos: list = field(default_factory=list)
