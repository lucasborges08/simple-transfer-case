from tests.utils.fake_user_repository import FakeUserRepository
from tests.utils.fake_tranfer_repository import FakeTransferRepository
from tests.utils.fake_authorizer import FakeAuthorizer
from tests.utils.fake_notifier import FakeNotifier
from app.services.transfer_input import TransferInput
from app.services.transfer_service import TransferService
from tests.database import clear_db
from app.workers.transfer_watcher import TransferWatcher
from unittest.mock import patch


def test_user_can_register_a_transfer_to_another_user(valid_common_user, valid_another_common_user):
    clear_db()
    user_data = FakeUserRepository()
    user_data.store(valid_common_user)
    user_data.store(valid_another_common_user)
    balance_before = valid_common_user.balance

    transfer_input = TransferInput(from_user=str(valid_common_user.id), to_user=str(valid_another_common_user.id), value=100)
    transfer = TransferService()
    transfer_data = FakeTransferRepository()

    stored_transfer_id = transfer.store(transfer_input)
    stored_transfer = transfer_data.find(stored_transfer_id)

    assert stored_transfer.from_user is not None
    assert user_data.find(str(valid_common_user.id)).balance == balance_before - stored_transfer.value


def test_canceled_transfer_must_refund_value(valid_common_user, valid_another_common_user):
    clear_db()
    user_data = FakeUserRepository()
    user_data.store(valid_common_user)
    user_data.store(valid_another_common_user)
    balance_before = valid_common_user.balance

    transfer_input = TransferInput(from_user=str(valid_common_user.id), to_user=str(valid_another_common_user.id),
                                   value=100)
    transfer = TransferService()
    transfer_data = FakeTransferRepository()

    stored_transfer_id = transfer.store(transfer_input)
    transfer.cancel(str(stored_transfer_id))
    stored_transfer = transfer_data.find(stored_transfer_id)

    assert stored_transfer.status == 'canceled'
    assert user_data.find(str(valid_common_user.id)).balance == balance_before


def test_completed_transfer_must_append_value_to_user_balance(valid_common_user, valid_another_common_user):
    clear_db()
    user_data = FakeUserRepository()
    user_data.store(valid_common_user)
    user_data.store(valid_another_common_user)

    balance_before = valid_another_common_user.balance

    transfer_input = TransferInput(from_user=str(valid_common_user.id), to_user=str(valid_another_common_user.id),
                                   value=100)
    transfer = TransferService()
    transfer_data = FakeTransferRepository()

    stored_transfer_id = transfer.store(transfer_input)
    transfer.complete(str(stored_transfer_id))
    stored_transfer = transfer_data.find(stored_transfer_id)

    assert stored_transfer.status == 'success'
    assert user_data.find(str(valid_another_common_user.id)).balance == balance_before + stored_transfer.value


@patch('app.workers.transfer_watcher.Authorizer')
def test_not_authorized_transaction_must_be_canceled(authorizer_mock, valid_common_user, valid_another_common_user):
    clear_db()
    fake_authorizer = FakeAuthorizer(False)
    authorizer_mock.return_value = fake_authorizer
    transfer_watcher = TransferWatcher()
    user_data = FakeUserRepository()
    user_data.store(valid_common_user)
    user_data.store(valid_another_common_user)

    transfer_input = TransferInput(from_user=str(valid_common_user.id), to_user=str(valid_another_common_user.id),
                                   value=100)
    transfer = TransferService()
    transfer_data = FakeTransferRepository()

    stored_transfer_id = transfer.store(transfer_input)
    stored_transfer = transfer_data.find(stored_transfer_id)
    transfer_watcher.process_transfer(stored_transfer)
    canceled_transfer = transfer_data.find(stored_transfer_id)

    assert canceled_transfer.status == 'canceled'
    assert fake_authorizer.authorization_return is False


@patch('app.workers.transfer_watcher.Authorizer')
@patch('app.workers.transfer_watcher.Notifier')
def test_authorized_transaction_must_be_notified(notifier_mock, authorizer_mock, valid_common_user, valid_another_common_user):
    clear_db()
    fake_notifier = FakeNotifier()
    fake_authorizer = FakeAuthorizer(True)
    authorizer_mock.return_value = fake_authorizer
    notifier_mock.return_value = fake_notifier
    transfer_watcher = TransferWatcher()
    user_data = FakeUserRepository()
    user_data.store(valid_common_user)
    user_data.store(valid_another_common_user)

    transfer_input = TransferInput(from_user=str(valid_common_user.id), to_user=str(valid_another_common_user.id),
                                   value=100)
    transfer = TransferService()
    transfer_data = FakeTransferRepository()

    stored_transfer_id = transfer.store(transfer_input)
    stored_transfer = transfer_data.find(stored_transfer_id)
    transfer_watcher.process_transfer(stored_transfer)
    canceled_transfer = transfer_data.find(stored_transfer_id)

    assert canceled_transfer.status == 'success'
    assert fake_authorizer.authorization_return is True
    assert fake_notifier.notified is True
