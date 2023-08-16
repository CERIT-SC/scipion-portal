
import logging
import requests

import logging


_host = 'https://datahub.egi.eu'

class Datahub:
    @staticmethod
    def _make_request(endpoint: str, oidc_token: str):
        headers = {'Authorization': f'Bearer egi:{oidc_token}'}
        response = requests.get(f'{_host}{endpoint}', headers=headers)

        data = ''
        error = ''

        if response.status_code != 200:
            error = f'Error, code: {response.status_code}, text: {response.text}'
        else:
            data = response.json()

        return (data, error)

    @staticmethod
    def list_spaces(oidc_token):
        return Datahub._make_request(f'/api/v3/onezone/user/spaces', oidc_token)

    @staticmethod
    def get_space(oidc_token, space_id):
        return Datahub._make_request(f'/api/v3/onezone/spaces/{space_id}', oidc_token)
