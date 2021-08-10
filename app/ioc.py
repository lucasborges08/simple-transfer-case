import os
from app.repositories.transfer_repository import TransferRepository
from app.repositories.user_respository import UserRepository
from tests.utils.fake_user_repository import FakeUserRepository
from tests.utils.fake_tranfer_repository import FakeTransferRepository

is_test_env = os.getenv('APP_ENV', '') == 'testing'


def get_repository(which):
    env_type = 'testing' if is_test_env else 'running'
    return repositories[env_type][which]


repositories = {
    'running': {
        'user': UserRepository(),
        'transfer': TransferRepository()
    },
    'testing': {
        'user': FakeUserRepository(),
        'transfer': FakeTransferRepository()
    }
}
