from app.domain.transfer import Transfer
from app.config import settings
import requests


class Authorizer:

    def authorize(self, _transfer: Transfer):
        response = requests.get(settings.AUTHORIZER_URL)
        if response.status_code != 200:
            raise Exception('authorizer unavailable')

        return response.json()['message'] == 'Autorizado'
