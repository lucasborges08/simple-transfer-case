from app.domain.user import User
from app.domain.base_entity import BaseEntity


class Transfer(BaseEntity):

    min_transfer_value = 0.01

    def __init__(self, from_user: User, to_user: User, value: float, status: str = 'pending'):
        super().__init__()

        self.from_user = from_user
        self.to_user = to_user
        self.value = value
        self.status = status

    def validate(self):
        if self.__is_from_store_keeper():
            raise Exception('Storekeeper cannot make transfers')

        if not self.__has_valid_value():
            raise Exception('Cannot transfer negative values')

        if not self.from_user.balance >= self.value:
            raise Exception('User does not have enough balance')

    def __is_from_store_keeper(self):
        return self.from_user.is_storekeeper

    def __has_valid_value(self):
        return self.value >= self.min_transfer_value
