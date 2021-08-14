from app.domain.user import User
from tests.database import get_db, update_db
from app.domain.exceptions.validation_exception import ValidationException


class FakeUserRepository:

    db_name = 'users'

    def __init__(self):
        DATABASE = get_db()
        if not DATABASE.get(self.db_name):
            DATABASE[self.db_name] = {'records': []}
        update_db(DATABASE)

    def store(self, user: User) -> bool:
        DATABASE = get_db()

        if list(filter(lambda u: str(u.email) == user.email, DATABASE[self.db_name]['records'])):
            raise ValidationException('Email already exists in database')

        if list(filter(lambda u: str(u.doc_number) == user.doc_number, DATABASE[self.db_name]['records'])):
            raise ValidationException('Document already exists in database')

        DATABASE[self.db_name]['records'].append(user)
        update_db(DATABASE)
        return user.id

    def find(self, user_id: str) -> User:
        DATABASE = get_db()
        return next(filter(lambda u: str(u.id) == user_id, DATABASE[self.db_name]['records']))

    def get_by_credentials(self, email: str, password: str) -> User:
        DATABASE = get_db()
        user = None
        for u in DATABASE[self.db_name]['records']:
            if u.email == email and u.password == password:
                return u

        raise Exception('Invalid credentials')


