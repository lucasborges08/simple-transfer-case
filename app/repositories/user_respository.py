from app.domain.user import User
from app.infrastructure.database import get_conn
from uuid import UUID


class UserRepository:
    def __init__(self):
        pass

    def store(self, user: User):
        return 10

    def find(self, user_id: str) -> User:
        with get_conn() as (conn, cursor):
            cursor.execute('SELECT id, name, email, doc_number, balance, is_storekeeper FROM users where id::text = %s limit 1', (user_id,))
            _return = cursor.fetchone()
            if not _return:
                raise Exception('User not found')

            return User(_id=UUID(_return['id']), name=_return['name'], email=_return['email'],
                        doc_number=_return['doc_number'], balance=_return['balance'])
