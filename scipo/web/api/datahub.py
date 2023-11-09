
import logging
import requests

import logging


logger = logging.getLogger('django')

_host = 'https://datahub.egi.eu'

class Datahub:
    @staticmethod
    def _make_request(endpoint: str, oidc_token: str):
        headers = {'Authorization': f'Bearer egi:{oidc_token}'}
        response = requests.get(f'{_host}{endpoint}', headers=headers)

        if response.status_code != 200:
            logger.error(f'Error, code: {response.status_code}, text: {response.text}')
            return None

        return response.json()

    @staticmethod
    def list_spaces(oidc_token):
        result = Datahub._make_request(f'/api/v3/onezone/user/effective_spaces', oidc_token)
        if not result:
            logger.error("Obtaining list of spaces failed.")

        return result

    @staticmethod
    def get_space(oidc_token, space_id):
        result = Datahub._make_request(f'/api/v3/onezone/spaces/{space_id}', oidc_token)
        if not result:
            logger.error("Obtaining list of spaces failed.")

        return result
