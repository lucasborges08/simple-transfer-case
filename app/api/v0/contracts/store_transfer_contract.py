from marshmallow import Schema
from marshmallow.fields import UUID, Float


class StoreTransferContract(Schema):
    from_user = UUID(required=True)
    to_user = UUID(required=True)
    value = Float(required=True)
