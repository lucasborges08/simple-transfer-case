

class FakeNotifier:

    def __init__(self):
        self.notified = False

    def notify(self, _user):
        self.notified = True
