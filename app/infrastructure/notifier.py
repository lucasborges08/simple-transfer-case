from app.domain.user import User
from app.config import settings
import requests


class Notifier:

    def notify(self, _user: User):
        # TODO: colocar a notificação como outro processo assíncrono
        response = requests.get(settings.NOTIFIER_URL)
        return response.json()
