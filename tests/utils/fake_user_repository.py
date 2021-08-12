from app.domain.user import User
from tests.database import get_db, update_db


class FakeUserRepository:

    db_name = 'users'

    def __init__(self):
        DATABASE = get_db()
        if not DATABASE.get(self.db_name):
            DATABASE[self.db_name] = {'records': []}
        update_db(DATABASE)

    def store(self, user: User) -> bool:
        DATABASE = get_db()
        DATABASE[self.db_name]['records'].append(user)
        update_db(DATABASE)
        return True

    def find(self, user_id: str) -> User:
        DATABASE = get_db()
        return next(filter(lambda u: str(u.id) == user_id, DATABASE[self.db_name]['records']))
