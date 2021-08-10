from app.services.transfer_input import TransferInput
from app.domain.transfer import Transfer
from app.ioc import get_repository


class TransferService:

    def __init__(self):
        self.transfer_data = get_repository('transfer')

    def store(self, transfer_input: TransferInput):
        transfer_obj = Transfer(transfer_input.from_user, transfer_input.to_user, transfer_input.value)
        return self.transfer_data.store(transfer_obj)
