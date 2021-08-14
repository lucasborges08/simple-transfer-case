from app.domain.user import User
from app.domain.base_entity import BaseEntity
from uuid import UUID
from app.domain.exceptions.validation_exception import ValidationException


class Transfer(BaseEntity):

    __min_transfer_value = 0.01

    def __init__(self, from_user: User, to_user: User, value: float, status: str = 'pending', _id: UUID = None):
        super().__init__(_id=_id)

        self.from_user = from_user
        self.to_user = to_user
        self.value = value
        self.status = status

    def validate(self):
        if self.__is_from_store_keeper():
            raise ValidationException('Storekeeper cannot make transfers')

        if not self.__has_valid_value():
            raise ValidationException('Cannot transfer negative values')

        if not self.from_user.balance >= self.value:
            raise ValidationException('User does not have enough balance')

    def __is_from_store_keeper(self):
        return self.from_user.is_storekeeper

    def __has_valid_value(self):
        return self.value >= self.__min_transfer_value
