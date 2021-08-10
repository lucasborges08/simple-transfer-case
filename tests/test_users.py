import pytest
from app.domain.user import User


def test_user_must_have_valid_cpf(valid_email, valid_name, valid_password):
    invalid_cpf = '111.111.111-11'
    with pytest.raises(Exception) as _exception:
        User(doc_number=invalid_cpf, email=valid_email, name=valid_name, password=valid_password)

    assert "Invalid CPF" in str(_exception.value)


def test_user_must_have_valid_email(valid_cpf, valid_name, valid_password):
    invalid_email = 'abc.com.br'
    with pytest.raises(Exception) as _exception:
        User(doc_number=valid_cpf, email=invalid_email, name=valid_name, password=valid_password)

    assert "Invalid email" in str(_exception.value)


def test_user_must_have_valid_cnpj(valid_email, valid_name, valid_password):
    invalid_cnpj = '11.111.111/0001-11'
    with pytest.raises(Exception) as _exception:
        User(doc_number=invalid_cnpj, email=valid_email, name=valid_name, password=valid_password)

    assert 'Invalid CNPJ' in str(_exception.value)


def test_name_must_have_min_length(valid_email, valid_cpf, valid_password):
    invalid_min_length_name = 'ab'
    with pytest.raises(Exception) as _exception:
        User(doc_number=valid_cpf, email=valid_email, name=invalid_min_length_name, password=valid_password)

    assert 'Invalid name min length' in str(_exception.value)


def test_password_must_have_min_length(valid_email, valid_cpf, valid_name):
    invalid_min_length_password = '3456'
    with pytest.raises(Exception) as _exception:
        User(doc_number=valid_cpf, email=valid_email, name=valid_name, password=invalid_min_length_password)

    assert 'Invalid password min length' in str(_exception.value)