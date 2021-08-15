from bottle import Bottle, HTTPResponse, request
from app.services.user_service import UserService
from app.services.user_store_input import UserStoreInput
from app.api.v0.contracts.store_user_contract import StoreUserContract
from marshmallow.exceptions import ValidationError
from app.domain.exceptions.validation_exception import ValidationException
from app.libs.auth_plugin import bypass_auth
from copy import deepcopy

user_resource = Bottle()


@user_resource.route('/', 'POST')
@bypass_auth
def store_user():
    try:
        data = deepcopy(request.json)
        StoreUserContract().load(data)
        transfer_input = UserStoreInput(name=data['name'], email=data['email'], doc_number=data['doc_number'], password=data['password'])
        stored_user_id = UserService().store(transfer_input)

        return HTTPResponse({'msg': {'id': str(stored_user_id)}}, status=200)
    except ValidationError as e:
        return HTTPResponse({'msg': e.messages}, status=422)
    except ValidationException as e:
        return HTTPResponse({'msg': str(e)}, status=422)
    except Exception as e:
        return HTTPResponse({'msg': str(e)}, status=500)
