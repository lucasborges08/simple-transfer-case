from app.domain.transfer import Transfer
from app.domain.user import User
from tests.utils.fake_user_repository import FakeUserRepository
from tests.utils.fake_tranfer_repository import FakeTransferRepository
from app.services.transfer_input import TransferInput
from app.services.transfer_service import TransferService


def test_user_can_make_a_transfer_to_another_user(valid_common_user, valid_another_common_user):
    user_data = FakeUserRepository()
    user_data.store(valid_common_user)
    user_data.store(valid_another_common_user)

    transfer_input = TransferInput(from_user=str(valid_common_user.id), to_user=valid_another_common_user.id, value=100)
    transfer = TransferService()
    transfer_data = FakeTransferRepository()

    stored_transfer_id = transfer.store(transfer_input)
    stored_transfer = transfer_data.find(stored_transfer_id)

    assert stored_transfer.from_user is not None
