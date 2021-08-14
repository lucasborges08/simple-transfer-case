from bottle import Bottle, HTTPResponse, request
from app.services.user_service import UserService
from app.services.user_store_input import UserStoreInput
from app.api.v0.contracts.store_user_contract import StoreUserContract
from marshmallow.exceptions import ValidationError

user_resource = Bottle()


@user_resource.route('/', 'POST')
def store_user():
    try:
        data = request.json
        StoreUserContract().load(data)
        transfer_input = UserStoreInput(name=data['name'], email=data['email'], doc_number=data['doc_number'],
                                        password=data['password'])
        UserService().store(transfer_input)
        return HTTPResponse({'msg': 'Ok'}, status=200)
    except ValidationError as e:
        return HTTPResponse({'msg': 'error', 'errors': e.messages}, status=422)
    except Exception as e:
        return HTTPResponse({'msg': str(e)}, status=400)