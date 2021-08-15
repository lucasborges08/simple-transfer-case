from bottle import Bottle, HTTPResponse, request
from app.services.auth_service import AuthService
from app.services.authenticate_input import AuthenticateInput
from app.libs.auth_plugin import bypass_auth

from app.api.v0.contracts.authenticate_contract import AuthenticateContract
from marshmallow.exceptions import ValidationError

auth_resource = Bottle()


@auth_resource.route('/', 'POST')
@bypass_auth
def authenticate():
    try:
        data = request.json
        AuthenticateContract().load(data)
        auth_input = AuthenticateInput(email=data['email'], password=data['password'])
        access_token = AuthService().authenticate(auth_input)
        return HTTPResponse({'access_token': access_token}, status=200)
    except ValidationError as e:
        return HTTPResponse({'msg': 'error', 'errors': e.messages}, status=422)
    except Exception as e:
        return HTTPResponse({'msg': str(e)}, status=400)

