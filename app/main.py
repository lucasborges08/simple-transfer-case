from bottle import Bottle
from app.api.v0.transfer_resource import transfer_resource
from app.api.v0.user_resource import user_resource

api = Bottle()
api.mount('/v0/transfers', transfer_resource)
api.mount('/v0/users', user_resource)

if __name__ == "__main__":
    api.run(host='0.0.0.0', port='8090')
