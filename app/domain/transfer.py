from app.domain.user import User


class Transfer:

    min_transfer_value = 0.01

    def __init__(self, from_user: User, to_user: User, value: float):
        self.from_user = from_user
        self.to_user = to_user
        self.value = value

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
