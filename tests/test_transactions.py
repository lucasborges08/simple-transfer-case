import pytest
from app.domain.user import User
from app.domain.transfer import Transfer


def test_storekeeper_cannot_make_transfer(valid_storekeeper_user, valid_common_user):
    transfer = Transfer(from_user=valid_storekeeper_user, to_user=valid_common_user, value=100.00)
    with pytest.raises(Exception) as _exception:
        transfer.validate()

    assert 'Storekeeper cannot make transfers' in str(_exception.value)


def test_cannot_transfer_negative_value(valid_common_user, valid_another_common_user):
    transfer = Transfer(from_user=valid_another_common_user, to_user=valid_common_user, value=-10)
    with pytest.raises(Exception) as _exception:
        transfer.validate()

    assert 'Cannot transfer negative values' in str(_exception.value)


def test_cannot_transfer_if_user_doesnt_have_enough_balance(valid_common_user, valid_email, valid_password,
                                                            valid_cpf, valid_name):
    user_with_no_enough_balance = User(doc_number=valid_cpf, email=valid_email, name=valid_name, password=valid_password)
    transfer = Transfer(from_user=user_with_no_enough_balance, to_user=valid_common_user, value=100)
    with pytest.raises(Exception) as _exception:
        transfer.validate()

    assert 'User does not have enough balance' in str(_exception.value)
