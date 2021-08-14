import bcrypt


class PasswordHelper:

    def make_hash(self, value, salt=None):
        salt_value = salt or bcrypt.gensalt(12)
        hash_value = bcrypt.hashpw(value.encode('utf-8'), salt_value)
        return hash_value.decode('utf-8'), salt_value.decode('utf-8')

    def check(self, hashed_password: str, raw_password: str):
        return bcrypt.checkpw(password=raw_password.encode('utf-8'), hashed_password=hashed_password.encode('utf-8'))
