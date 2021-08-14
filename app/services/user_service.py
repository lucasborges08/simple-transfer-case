from app.services.user_store_input import UserStoreInput
from app.domain.user import User
from app.ioc import get_repository


class UserService:

    def __init__(self):
        self.user_data = get_repository('user')

    def store(self, transfer_input: UserStoreInput):
        user = User(name=transfer_input.name, doc_number=transfer_input.doc_number, email=transfer_input.email,
                    password=transfer_input.password)

        user.validate()
        return self.user_data.store(user)
