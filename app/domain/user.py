from validate_docbr import CPF, CNPJ
from email_validator import validate_email, EmailNotValidError
import re


class User:

    min_name_length = 3
    min_password_length = 6

    def __init__(self, doc_number: str, email: str, name: str, password: str):
        sanitized_doc_number = self.__sanitize_doc_number(doc_number)
        is_cnpj = len(sanitized_doc_number) > 11
        if is_cnpj:
            if not CNPJ().validate(sanitized_doc_number):
                raise Exception('Invalid CNPJ')
        elif not CPF().validate(sanitized_doc_number):
            raise Exception('Invalid CPF')

        try:
            validate_email(email)
        except EmailNotValidError:
            raise Exception('Invalid email')

        if len(name) < self.min_name_length:
            raise Exception('Invalid name min length')

        if len(password) < self.min_password_length:
            raise Exception('Invalid password min length')

        self.doc_number = sanitized_doc_number
        self.is_storekeeper = is_cnpj
        self.email = email
        self.name = name
        self.password = password

    def __sanitize_doc_number(self, doc_number):
        return re.sub('[-. /]', '', doc_number)
