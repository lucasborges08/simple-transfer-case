from app.domain.transfer import Transfer
from app.infrastructure.database import get_conn
from app.domain.user import User
from uuid import UUID


class TransferRepository:

    def __init__(self):
        pass

    def store(self, transfer: Transfer):
        with get_conn() as (conn, cursor):
            cursor.execute('INSERT INTO transfers VALUES(%s,%s,%s,%s,%s,now(),now());',
                           (str(transfer.id), str(transfer.from_user.id), str(transfer.to_user.id),
                            transfer.value, transfer.status))
            cursor.execute('UPDATE users set balance = balance - %s where id = %s',
                           (transfer.value, str(transfer.from_user.id)))

        return transfer.id

    def find(self, transfer_id: str) -> Transfer:
        with get_conn() as (conn, cursor):
            cursor.execute('SELECT t.id, t.from_user_id, t.to_user_id, t.value, t.status,'
                           '   from_user.name as fu_name, from_user.email as fu_email,'
                           '   from_user.doc_number as fu_doc_number, from_user.balance as fu_balance,'
                           '   to_user.name as tu_name, to_user.email as tu_email, '
                           '   to_user.doc_number as tu_doc_number, to_user.balance as tu_balance '
                           'FROM transfers t ' 
                           'inner join users from_user on t.from_user_id = from_user.id '
                           'inner join users to_user on t.to_user_id = to_user.id'
                           'where t.id = %s;',
                           (transfer_id,))
            _ret = cursor.fetchone()
            if not _ret:
                raise Exception('Transfer not found')

            from_user = User(_id=UUID(_ret['from_user_id']), name=_ret['fu_name'], email=_ret['fu_email'],
                             doc_number=_ret['fu_doc_number'], balance=_ret['fu_balance'])
            to_user = User(_id=UUID(_ret['from_user_id']), name=_ret['tu_name'], email=_ret['tu_email'],
                             doc_number=_ret['tu_doc_number'], balance=_ret['tu_balance'])

            return Transfer(_id=_ret['id'], from_user=from_user, to_user=to_user, status=_ret['status'],
                            value=_ret['value'])

    def cancel(self, transfer_id: str) -> bool:
        with get_conn() as (conn, cursor):
            cursor.execute("UPDATE transfers SET status = 'canceled', updated_at = now() "
                           "where id = %s RETURNING value, from_user_id",
                           (transfer_id,))
            _ret = cursor.fetchone()
            cursor.execute('UPDATE users set balance = balance + %s, updated_at = now() where id = %s',
                           (_ret[0], _ret[1]))

        return True

    def complete(self, transfer_id: str) -> bool:
        with get_conn() as (conn, cursor):
            cursor.execute("UPDATE transfers SET status = 'success', updated_at = now() "
                           "where id = %s RETURNING value, to_user_id",
                           (transfer_id,))
            _ret = cursor.fetchone()
            cursor.execute('UPDATE users set balance = balance + %s, updated_at = now() where id = %s',
                           (_ret[0], _ret[1]))

        return True

    def get_pending_raw(self, limit=100) -> list:
        with get_conn() as (conn, cursor):
            cursor.execute("SELECT t.id, t.from_user_id, t.to_user_id, t.value, t.status,"
                           "   from_user.name as fu_name, from_user.email as fu_email,"
                           "   from_user.doc_number as fu_doc_number, from_user.balance as fu_balance,"
                           "   to_user.name as tu_name, to_user.email as tu_email, "
                           "   to_user.doc_number as tu_doc_number, to_user.balance as tu_balance "
                           "FROM transfers t "
                           "inner join users from_user on t.from_user_id = from_user.id "
                           "inner join users to_user on t.to_user_id = to_user.id "
                           "where t.status = 'pending'"
                           )
            _ret = []
            for _transfer in cursor.fetchall():
                transfer = dict(_transfer)
                from_user = User(_id=UUID(transfer['from_user_id']), name=transfer['fu_name'], email=transfer['fu_email'],
                                 doc_number=transfer['fu_doc_number'], balance=transfer['fu_balance'])
                to_user = User(_id=UUID(transfer['from_user_id']), name=transfer['tu_name'], email=transfer['tu_email'],
                               doc_number=transfer['tu_doc_number'], balance=transfer['tu_balance'])

                _ret.append(Transfer(_id=transfer['id'], from_user=from_user, to_user=to_user,
                                     status=transfer['status'], value=transfer['value']))

            return _ret
