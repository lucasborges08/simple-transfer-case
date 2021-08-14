from app.domain.user import User
from app.infrastructure.database import get_conn
from app.infrastructure.password_helper import PasswordHelper
from app.domain.exceptions.validation_exception import ValidationException
from uuid import UUID
from psycopg2.errors import lookup


class UserRepository:
    def __init__(self):
        self.password_helper = PasswordHelper()
        pass

    def store(self, user: User):
        with get_conn() as (conn, cursor):
            try:
                hashed_pass, salt = self.password_helper.make_hash(user.password)
                cursor.execute(
                    'INSERT INTO users values (%s,%s,%s,%s,%s,%s,%s,%s, now(), now())',
                    (str(user.id), user.name, user.email, user.doc_number, user.balance, user.is_storekeeper,
                     hashed_pass, salt))

                return user.id
            except lookup('23505') as e:
                if 'Key (email)' in e.pgerror:
                    raise ValidationException('Email already exists in database')
                if 'Key (doc_number)' in e.pgerror:
                    raise ValidationException('Document already exists in database')

    def find(self, user_id: str) -> User:
        with get_conn() as (conn, cursor):
            cursor.execute('SELECT id, name, email, doc_number, balance, is_storekeeper FROM users where id::text = %s limit 1', (user_id,))
            _return = cursor.fetchone()
            if not _return:
                raise Exception('User not found')

            return User(_id=UUID(_return['id']), name=_return['name'], email=_return['email'],
                        doc_number=_return['doc_number'], balance=_return['balance'])

    def get_by_credentials(self, email: str, password: str) -> User:
        with get_conn() as (conn, cursor):
            cursor.execute(
                'SELECT id, name, email, doc_number, balance, is_storekeeper, password, password_salt FROM users where email = %s limit 1',
                (email,))
            _return = cursor.fetchone()
            if not _return or not self.password_helper.check(_return['password'], password):
                raise Exception('Invalid credentials')

            return User(_id=UUID(_return['id']), name=_return['name'], email=_return['email'],
                        doc_number=_return['doc_number'], balance=_return['balance'])
