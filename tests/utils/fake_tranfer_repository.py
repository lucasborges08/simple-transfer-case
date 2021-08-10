from app.domain.transfer import Transfer
from tests.database import DATABASE


class FakeTransferRepository:

    db_name = 'transactions'

    def __init__(self):
        if not DATABASE.get(self.db_name):
            DATABASE[self.db_name] = {'records': []}

    def store(self, transfer: Transfer):
        DATABASE[self.db_name]['records'].append(transfer)
        return transfer.id

    def find(self, transfer_id: str) -> Transfer:
        return next(filter(lambda t: t.id == transfer_id, DATABASE[self.db_name]['records']))

