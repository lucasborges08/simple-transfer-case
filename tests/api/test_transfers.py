from tests.database import clear_db
from tests.utils.fake_user_repository import FakeUserRepository
from app.services.auth_service import AuthService
from app.services.authenticate_input import AuthenticateInput


def test_user_must_request_transfer_to_another_user(api_client, valid_common_user, valid_another_common_user):
    clear_db()
    auth_service = AuthService()
    user_data = FakeUserRepository()
    user_data.store(valid_common_user)
    user_data.store(valid_another_common_user)

    balance_before = user_data.find(str(valid_common_user.id)).balance

    body = {
        "from_user": str(valid_common_user.id),
        "to_user": str(valid_another_common_user.id),
        "value": 10.00
    }

    auth_input = AuthenticateInput(email=valid_common_user.email, password=valid_common_user.password)
    token = auth_service.authenticate(auth_input)
    result = api_client.post_json('/v0/transfers', body, headers={'Authorization': 'Bearer ' + token})
    balance_after = user_data.find(str(valid_common_user.id)).balance

    assert result.status_int == 200
    assert balance_after == balance_before - body['value']


def test_storekeeper_trying_to_transfer_money_fails(api_client, valid_storekeeper_user, valid_common_user):
    clear_db()
    auth_service = AuthService()
    user_data = FakeUserRepository()
    user_data.store(valid_common_user)
    user_data.store(valid_storekeeper_user)

    body = {
        "from_user": str(valid_storekeeper_user.id),
        "to_user": str(valid_common_user.id),
        "value": 10.00
    }

    auth_input = AuthenticateInput(email=valid_storekeeper_user.email, password=valid_storekeeper_user.password)
    token = auth_service.authenticate(auth_input)
    result = api_client.post_json('/v0/transfers', body, headers={'Authorization': 'Bearer ' + token},
                                  expect_errors=True)

    assert result.status_int == 400
    assert result.json['msg'] == 'Storekeeper cannot make transfers'


def test_transfer_with_wrong_contract_fails(api_client, valid_common_user):
    auth_service = AuthService()

    body = {
        "_from_user": '',
        "_to_user": '',
        "_value": 10.00
    }

    auth_input = AuthenticateInput(email=valid_common_user.email, password=valid_common_user.password)
    token = auth_service.authenticate(auth_input)
    result = api_client.post_json('/v0/transfers', body, headers={'Authorization': 'Bearer ' + token},
                                  expect_errors=True)
    
    assert result.status_int == 422

