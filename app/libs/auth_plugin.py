from bottle import request, abort
import inspect
import jwt
import logging


class AuthPlugin:

    def __init__(self, secret=None, algorithm=None, user_id_kw='jwt_user_id'):
        self.secret = secret or 'secret'
        self.algorithm = algorithm or 'HS256'
        self.user_id_kw = user_id_kw

    def setup(self, app):
        pass

    def apply(self, callback, _context):
        callback_args = inspect.signature(callback).parameters.keys()

        def wrapper(*args, **kwargs):
            auth_header = request.headers.get('Authorization', '')

            if hasattr(callback, 'bypass_auth'):
                return callback(*args, **kwargs)

            if not auth_header.startswith('Bearer'):
                abort(401, 'No authorization header found')

            try:
                token = auth_header.split(' ')[1]
                decoded_token = jwt.decode(token, self.secret, algorithms=self.algorithm)
            except Exception as e:
                logging.error(str(e))
                logging.info(auth_header)
                abort(401, 'Expired token')

            if self.user_id_kw in callback_args:
                kwargs[self.user_id_kw] = decoded_token['user']['id']

            return callback(*args, **kwargs)

        return wrapper


def bypass_auth(callback):
    callback.bypass_auth = True
    return callback
