from validate_docbr import CPF, CNPJ
from email_validator import validate_email, EmailNotValidError
from app.domain.base_entity import BaseEntity
from app.domain.exceptions.validation_exception import ValidationException
from uuid import UUID
import re


class User(BaseEntity):

    min_name_length = 3
    min_password_length = 6

    def __init__(self, doc_number: str, email: str, name: str, password: str = '',
                 balance: float = 0.0, _id: UUID = None):
        super().__init__(_id=_id)
        sanitized_doc_number = self.__sanitize_doc_number(doc_number)
        is_cnpj = len(sanitized_doc_number) > 11
        if is_cnpj:
            if not CNPJ().validate(sanitized_doc_number):
                raise ValidationException('Invalid CNPJ')
        elif not CPF().validate(sanitized_doc_number):
            raise ValidationException('Invalid CPF')

        try:
            validate_email(email)
        except EmailNotValidError:
            raise ValidationException('Invalid email')

        if len(name) < self.min_name_length:
            raise ValidationException('Invalid name min length')

        self.doc_number = sanitized_doc_number
        self.is_storekeeper = is_cnpj
        self.email = email
        self.name = name
        self.password = password
        self.balance = balance

    def validate(self):
        if len(self.password) < self.min_password_length:
            raise ValidationException('Invalid password min length')

    def __sanitize_doc_number(self, doc_number):
        return re.sub('[-. /]', '', doc_number)
