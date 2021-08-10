from pytest import fixture


@fixture(scope='function')
def valid_cpf():
    return '600.993.600-47'


@fixture(scope='function')
def valid_email():
    return 'email@email.com'


@fixture(scope='function')
def valid_name():
    return 'joão da silva'


@fixture(scope='function')
def valid_password():
    return '123456'
