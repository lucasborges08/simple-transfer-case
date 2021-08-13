from uuid import uuid4


class BaseEntity:

    def __init__(self, _id=None):
        self.id = _id or uuid4()
