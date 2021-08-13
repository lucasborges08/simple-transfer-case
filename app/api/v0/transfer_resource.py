from bottle import Bottle, HTTPResponse, request
from app.services.transfer_service import TransferService
from app.services.transfer_service import TransferInput
from app.api.v0.contracts.store_transfer_contract import StoreTransferContract
from marshmallow.exceptions import ValidationError

transfer_resource = Bottle()


@transfer_resource.route('/transfers', 'POST')
def store_transfer():
    try:
        data = request.json
        StoreTransferContract().load(data)
        transfer_input = TransferInput(from_user=data['from_user'], to_user=data['to_user'], value=float(data['value']))
        TransferService().store(transfer_input)
        return HTTPResponse({'msg': 'Ok'}, status=200)
    except ValidationError as e:
        return HTTPResponse({'msg': 'error', 'errors': e.messages}, status=422)
    except Exception as e:
        return HTTPResponse({'msg': str(e)}, status=400)
