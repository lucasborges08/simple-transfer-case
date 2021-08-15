from app.services.transfer_input import TransferInput
from app.domain.transfer import Transfer
from app.ioc import get_repository


class TransferService:

    def __init__(self):
        self.transfer_data = get_repository('transfer')
        self.user_data = get_repository('user')

    def store(self, transfer_input: TransferInput, requester_id):
        if not requester_id == transfer_input.from_user:
            raise Exception('Inconsistent User')
        from_user = self.user_data.find(transfer_input.from_user)
        to_user = self.user_data.find(transfer_input.to_user)

        transfer_obj = Transfer(from_user, to_user, transfer_input.value)
        transfer_obj.validate()
        return self.transfer_data.store(transfer_obj)

    def cancel(self, transfer_id: str):
        return self.transfer_data.cancel(transfer_id)

    def get_pending(self):
        return self.transfer_data.get_pending_raw()

    def complete(self, transfer_id: str):
        return self.transfer_data.complete(transfer_id)
