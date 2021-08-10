import pytest
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
