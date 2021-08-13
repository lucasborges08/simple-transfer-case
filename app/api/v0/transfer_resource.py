from bottle import Bottle, HTTPResponse, request
from app.services.transfer_service import TransferService
from app.services.transfer_service import TransferInput

transfer_resource = Bottle()


@transfer_resource.route('/transfers', 'POST')
def store_transfer():
    data = request.json
    if not data:
        return HTTPResponse({'msg': 'empty body'}, status=400)

    try:
        transfer_input = TransferInput(from_user=data['from_user'], to_user=data['to_user'], value=float(data['value']))
        TransferService().store(transfer_input)
        return HTTPResponse({'msg': 'Ok'}, status=200)
    except Exception as e:
        return HTTPResponse({'msg': str(e)}, status=400)
