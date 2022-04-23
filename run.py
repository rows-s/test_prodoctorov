from src.report import UsersStream
from src.apis import MedRatingAPI
from src.handlers import FileHandler


def main():
    file_handler = FileHandler()
    for user in UsersStream(MedRatingAPI()):
        file_handler.handle_report(user)


if __name__ == '__main__':
    main()
