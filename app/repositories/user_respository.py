from app.domain.user import User
from app.infrastructure.database import get_conn
from app.infrastructure.password_helper import PasswordHelper
from uuid import UUID


class UserRepository:
    def __init__(self):
        self.password_helper = PasswordHelper()
        pass

    def store(self, user: User):
        with get_conn() as (conn, cursor):
            hashed_pass, salt = self.password_helper.make_hash(user.password)
            cursor.execute(
                'INSERT INTO users values (%s,%s,%s,%s,%s,%s,%s,%s, now(), now())',
                (str(user.id), user.name, user.email, user.doc_number, user.balance, user.is_storekeeper,
                 hashed_pass, salt))

            return user.id

    def find(self, user_id: str) -> User:
        with get_conn() as (conn, cursor):
            cursor.execute('SELECT id, name, email, doc_number, balance, is_storekeeper FROM users where id::text = %s limit 1', (user_id,))
            _return = cursor.fetchone()
            if not _return:
                raise Exception('User not found')

            return User(_id=UUID(_return['id']), name=_return['name'], email=_return['email'],
                        doc_number=_return['doc_number'], balance=_return['balance'])
