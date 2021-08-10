from uuid import uuid4


class BaseEntity:
    id = uuid4()

    def __init__(self):
        pass

