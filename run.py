from src.apis import MedRatingAPI
from src.report import UserReport
from src.streams import UserReportsStream
from src.handlers import FileHandlerWithArchiving


def main():
    file_handler = FileHandlerWithArchiving(directory='tasks')
    for user in UserReportsStream(MedRatingAPI()):
        file_handler.handle_report(user)


if __name__ == '__main__':
    main()
