import bcrypt


class PasswordHelper:

    __iterations = 100000
    __keylen = 128

    def make_hash(self, value, salt=None):
        salt_value = salt or bcrypt.gensalt(12)
        hash_value = bcrypt.hashpw(value.encode('utf-8'), salt_value)
        return hash_value.decode('utf-8'), salt_value.decode('utf-8')

    def check(self, hashed_password, raw_password, salt):
        return hashed_password == self.make_hash(raw_password, salt)
