from marshmallow import Schema
from marshmallow.fields import UUID, Float, String


class StoreUserContract(Schema):
    name = String(required=True)
    email = String(required=True)
    doc_number = String(required=True)
    password = String(required=True)
