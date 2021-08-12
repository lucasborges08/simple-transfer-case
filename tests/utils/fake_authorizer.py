from app.domain.transfer import Transfer


class FakeAuthorizer:

    def __init__(self, must_authorize=True):
        self.must_authorize = must_authorize
        self.authorization_return = None

    def authorize(self, _transfer: Transfer):
        self.authorization_return = self.must_authorize
        return self.must_authorize
