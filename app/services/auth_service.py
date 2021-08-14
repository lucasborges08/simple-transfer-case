from app.ioc import get_repository
from app.services.authenticate_input import AuthenticateInput
from datetime import datetime, timedelta
import jwt


class AuthService:

    def __init__(self):
        self.jwt_secret = 'secret'
        self.jwt_algorithm = 'HS256'
        self.user_data = get_repository('user')

    def authenticate(self, auth_input: AuthenticateInput):
        user = self.user_data.get_by_credentials(email=auth_input.email, password=auth_input.password)
        now = datetime.now()
        exp = now + timedelta(hours=10)
        return jwt.encode({'user': {'id': str(user.id), 'name': user.name, 'email': user.email},
                           'iat': datetime.timestamp(now),
                           'exp': datetime.timestamp(exp)},
                          self.jwt_secret,
                          algorithm=self.jwt_algorithm)

