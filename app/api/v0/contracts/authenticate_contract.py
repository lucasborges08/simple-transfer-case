from marshmallow import Schema
from marshmallow.fields import String


class AuthenticateContract(Schema):
    email = String(required=True)
    password = String(required=True)
