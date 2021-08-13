from app.services.transfer_service import TransferService
from app.infrastructure.authorizer import Authorizer
from app.infrastructure.notifier import Notifier
from time import sleep


class TransferWatcher:
    def __init__(self):
        self.transfer = TransferService()
        self.authorizer = Authorizer()
        self.notifier = Notifier()

    def process_transfer(self, transfer):
        if not self.authorizer.authorize(transfer):
            return self.transfer.cancel(str(transfer.id))

        self.transfer.complete(str(transfer.id))
        self.notifier.notify(transfer.to_user)

    def run_poll(self):
        while True:
            results = self.transfer.get_pending()
            if not results:
                sleep(3)
                continue

            for transfer in results:
                self.process_transfer(transfer)


if __name__ == '__main__':
    TransferWatcher().run_poll()
