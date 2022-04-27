from src.apis import MedRatingAPI
from src.report import UserReport
from src.streams import UsersStream
from src.handlers import FileHandlerWithArchiving


def main():
    file_handler = FileHandlerWithArchiving(directory='tasks')
    for user in UsersStream(MedRatingAPI(), user_cls=UserReport):
        file_handler.handle_report(user)  # noqa


if __name__ == '__main__':
    main()
