from tests.database import clear_db
from tests.utils.fake_user_repository import FakeUserRepository


def test_user_must_be_able_to_signup(api_client, valid_common_user):
    clear_db()
    user_data = FakeUserRepository()

    body = {
        "name": valid_common_user.name,
        "email": valid_common_user.email,
        "doc_number": valid_common_user.doc_number,
        "password": valid_common_user.password
    }
    result = api_client.post_json('/v0/users', body)
    stored_user = user_data.find(result.json['msg']['id'])

    assert result.status_int == 200
    assert stored_user.name == body['name']
    assert stored_user.email == body['email']
    assert stored_user.doc_number == body['doc_number']


def test_user_must_not_be_able_to_signup_with_email_that_already_exists(api_client, valid_common_user):
    clear_db()
    user_data = FakeUserRepository()
    user_data.store(valid_common_user)

    body = {
        "name": valid_common_user.name,
        "email": valid_common_user.email,
        "doc_number": valid_common_user.doc_number,
        "password": valid_common_user.password
    }
    result = api_client.post_json('/v0/users', body, expect_errors=True)

    assert result.status_int == 422
    assert 'Email already exists in database' in result.json['msg']


def test_user_must_not_be_able_to_signup_with_doc_number_that_already_exists(api_client, valid_common_user):
    clear_db()
    user_data = FakeUserRepository()
    user_data.store(valid_common_user)

    body = {
        "name": valid_common_user.name,
        "email": 'new' + valid_common_user.email,
        "doc_number": valid_common_user.doc_number,
        "password": valid_common_user.password
    }
    result = api_client.post_json('/v0/users', body, expect_errors=True)

    assert result.status_int == 422
    assert 'Document already exists in database' in result.json['msg']


def test_wrong_signup_request_contract_must_fail(api_client, valid_common_user):
    clear_db()
    body = {
        "_name": valid_common_user.name,
        "_email": valid_common_user.email,
        "_doc_number": valid_common_user.doc_number,
        "_password": valid_common_user.password
    }
    result = api_client.post_json('/v0/users', body, expect_errors=True)

    assert result.status_int == 422
