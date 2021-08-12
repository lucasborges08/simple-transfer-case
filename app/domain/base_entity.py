from uuid import uuid4


class BaseEntity:

    def __init__(self):
        self.id = uuid4()

