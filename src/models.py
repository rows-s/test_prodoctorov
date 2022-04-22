from dataclasses import dataclass, field

__all__ = ['Geo', 'Address', 'Company', 'User', 'Todo']


@dataclass
class Geo(Model):
    lat: str
    lng: str


@dataclass
class Address(Model):
    street: str
    suite: str
    city: str
    zipcode: str
    geo: Geo


@dataclass
class Company(Model):
    name: str
    catch_phrase: str
    bs: str

    __camel_to_snake_fields__ = {'catchPhrase': 'catch_phrase'}


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


@dataclass
class Todo(Model):
    id: int
    user_id: int
    title: str
    completed: bool

    __camel_to_snake_fields__ = {'userId': 'user_id'}
