

class UserStoreInput:

    def __init__(self, name: str, email: str, doc_number: str, password: str):
        self.name = name
        self.email = email
        self.doc_number = doc_number
        self.password = password
