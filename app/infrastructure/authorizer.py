from app.domain.transfer import Transfer
import requests


class Authorizer:

    def authorize(self, _transfer: Transfer):
        response = requests.get('https://run.mocky.io/v3/8fafdd68-a090-496f-8c9a-3442cf30dae6')
        if response.status_code != 200:
            raise Exception('authorizer unavailable')

        return response.json()['message'] == 'Autorizado'
