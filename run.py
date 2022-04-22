from src.report import UsersData
from src.apis import MedRatingAPI


def main():
    mr_api = MedRatingAPI()
    for user in UsersData(mr_api):
        print(user.id, user.todos)


if __name__ == '__main__':
    main()
