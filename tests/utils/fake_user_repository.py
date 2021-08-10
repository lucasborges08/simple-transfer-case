from app.domain.user import User
from tests.database import DATABASE


class FakeUserRepository:

    db_name = 'users'

    def __init__(self):
        if not DATABASE.get(self.db_name):
            DATABASE[self.db_name] = {'records': []}

    def store(self, user: User) -> bool:
        DATABASE[self.db_name]['records'].append(user)
        return True

    def find(self, user_id: str) -> User:
        return next(filter(lambda u: u.id == user_id, DATABASE[self.db_name]['records']))
