from app.domain.user import User
import requests


class Notifier:

    def notify(self, _user: User):
        # TODO: colocar a notificação como outro processo assíncrono
        response = requests.get('http://o4d9z.mocklab.io/notify')
        return response.json()
