from pytest import fixture
from app.domain.user import User


@fixture(scope='function')
def valid_cpf():
    return '600.993.600-47'


@fixture(scope='function')
def valid_cnpj():
    return '89.992.927/0001-69'


@fixture(scope='function')
def valid_email():
    return 'email@email.com'


@fixture(scope='function')
def valid_name():
    return 'joão da silva'


@fixture(scope='function')
def valid_password():
    return '123456'


@fixture(scope='function')
def valid_storekeeper_user(valid_cnpj, valid_name, valid_email, valid_password):
    return User(name=valid_name, doc_number=valid_cnpj, email=valid_email, password=valid_password)


@fixture(scope='function')
def valid_common_user(valid_cpf, valid_name, valid_email, valid_password):
    return User(name=valid_name, doc_number=valid_cpf, email=valid_email, password=valid_password, balance=500)


@fixture(scope='function')
def valid_another_common_user(valid_cpf, valid_name, valid_email, valid_password):
    return User(name=valid_name, doc_number=valid_cpf, email=valid_email, password=valid_password)


# @fixture(scope='function')
# def clear_fake_db():
#     from tests.database import DATABASE
#     DATABASE = {}
