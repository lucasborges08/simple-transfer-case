from bottle import Bottle
from app.api.v0.transfer_resource import transfer_resource

api = Bottle()
api.mount('/v0', transfer_resource)

if __name__ == "__main__":
    api.run(host='0.0.0.0', port='8090')
