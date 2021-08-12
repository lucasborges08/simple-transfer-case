from app.domain.transfer import Transfer
from tests.database import get_db, update_db


class FakeTransferRepository:

    db_name = 'transactions'
    db_user = 'users'

    def __init__(self):
        DATABASE = get_db()
        if not DATABASE.get(self.db_name):
            DATABASE[self.db_name] = {'records': []}
        update_db(DATABASE)

    def store(self, transfer: Transfer):
        DATABASE = get_db()
        DATABASE[self.db_name]['records'].append(transfer)

        idx = None
        user = None
        for i, u in enumerate(DATABASE[self.db_user]['records']):
            if str(u.id) == str(transfer.from_user.id):
                idx = i
                user = u
                break

        user.balance -= transfer.value
        DATABASE[self.db_user]['records'][idx] = user

        update_db(DATABASE)
        return transfer.id

    def find(self, transfer_id: str) -> Transfer:
        DATABASE = get_db()
        return next(filter(lambda t: t.id == transfer_id, DATABASE[self.db_name]['records']))

    def cancel(self, transfer_id: str) -> bool:
        DATABASE = get_db()
        idx = None
        transfer = None
        user = None
        for i, t in enumerate(DATABASE[self.db_name]['records']):
            if str(t.id) == transfer_id:
                idx = i
                transfer = t
                break

        transfer.status = 'canceled'
        DATABASE[self.db_name]['records'][idx] = transfer

        for i, u in enumerate(DATABASE[self.db_user]['records']):
            if str(u.id) == str(transfer.from_user.id):
                idx = i
                user = u
                break

        user.balance += transfer.value
        DATABASE[self.db_user]['records'][idx] = user
        update_db(DATABASE)
        return True

    def complete(self, transfer_id: str) -> bool:
        DATABASE = get_db()
        idx = None
        transfer = None
        user = None
        for i, t in enumerate(DATABASE[self.db_name]['records']):
            if str(t.id) == transfer_id:
                idx = i
                transfer = t
                break

        transfer.status = 'success'
        DATABASE[self.db_name]['records'][idx] = transfer

        for i, u in enumerate(DATABASE[self.db_user]['records']):
            if str(u.id) == str(transfer.to_user.id):
                idx = i
                user = u
                break

        user.balance += transfer.value
        DATABASE[self.db_user]['records'][idx] = user
        update_db(DATABASE)
        return True

    def get_pending(self) -> list:
        DATABASE = get_db()
        return list(filter(lambda t: t.status == 'pending', DATABASE[self.db_name]['records']))
