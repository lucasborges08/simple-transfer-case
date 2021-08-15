from bottle import Bottle
from app.libs.auth_plugin import AuthPlugin
from app.api.v0.transfer_resource import transfer_resource
from app.api.v0.user_resource import user_resource
from app.api.v0.auth_resource import auth_resource
import bottle
import json

api = Bottle()

transfer_resource.install(AuthPlugin())
user_resource.install(AuthPlugin())
auth_resource.install(AuthPlugin())

api.mount('/v0/transfers', transfer_resource)
api.mount('/v0/users', user_resource)
api.mount('/v0/authentication', auth_resource)


def handle_error_json(error):
    bottle.response.content_type = 'application/json'
    return json.dumps({'msg': str(error.body)})


error_handler_config = {
    401: handle_error_json,
    500: handle_error_json
}

transfer_resource.error_handler = error_handler_config
user_resource.error_handler = error_handler_config
auth_resource.error_handler = error_handler_config


if __name__ == "__main__":
    api.run(host='0.0.0.0', port='8090')
