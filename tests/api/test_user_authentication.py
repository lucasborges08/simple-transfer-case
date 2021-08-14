from tests.database import clear_db
from tests.utils.fake_user_repository import FakeUserRepository
from app.services.auth_service import AuthService
import jwt


def test_user_authentication_must_return_access_token(api_client, valid_common_user):
    clear_db()
    user_data = FakeUserRepository()
    user_data.store(valid_common_user)

    body = {
        "email": valid_common_user.email,
        "password": valid_common_user.password
    }
    result = api_client.post_json('/v0/authentication', body)

    assert result.status_int == 200
    auth_service = AuthService()
    user_from_token = jwt.decode(result.json['access_token'], auth_service.jwt_secret,
                                 algorithms=auth_service.jwt_algorithm)['user']
    assert user_from_token['id'] == str(valid_common_user.id)
    assert user_from_token['name'] == str(valid_common_user.name)
    assert user_from_token['email'] == str(valid_common_user.email)


def test_user_authentication_with_wrong_credentials_must_fail(api_client, valid_common_user):
    clear_db()
    user_data = FakeUserRepository()
    user_data.store(valid_common_user)

    body = {
        "email": valid_common_user.email + 'x',
        "password": valid_common_user.password + 'x'
    }
    result = api_client.post_json('/v0/authentication', body, expect_errors=True)

    assert result.status_int == 400
    assert result.json['msg'] == 'Invalid credentials'
