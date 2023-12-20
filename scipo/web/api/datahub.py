
import logging
import requests

from datetime import datetime, timedelta


logger = logging.getLogger('django')

_host = 'https://datahub.egi.eu'

class Datahubctl:

    class CacheEntry:
        def __init__(self, expiration, id, object) -> None:
            self.expiration = expiration
            self.id = id
            self.object = object

    cached_spaces = list()
    cached_providers = list()

    def _make_request_get(self, endpoint: str, oidc_token: str):
        headers = {'Authorization': f'Bearer egi:{oidc_token}'}
        response = requests.get(f'{_host}{endpoint}', headers=headers)

        if response.status_code != 200:
            logger.error(f'Error, code: {response.status_code}, text: {response.text}')
            return None

        return response.json()

    def _make_request_post(self, endpoint: str, oidc_token: str, data: dict):
        headers = {
            'Authorization': f'Bearer egi:{oidc_token}',
            'Content-type': 'application/json'
        }
        response = requests.post(f'{_host}{endpoint}', json=data, headers=headers)

        if response.status_code != 201:
            logger.error(f'Error, code: {response.status_code}, text: {response.text}')
            return None

        return response.json()

    def generate_temp_token(self, oidc_token):
        data = {
            "type": {
                "accessToken": {}
            },
            "caveats": [{
                "type": "time",
                "validUntil": (int)((datetime.now() + timedelta(days=30)).timestamp())
            }]
        }
        result = self._make_request_post("/api/v3/onezone/user/tokens/temporary", oidc_token, data)
        if not result:
            logger.error("Generating temporary token failed.")

        return result["token"]

    def list_spaces(self, oidc_token):
        result = self._make_request_get(f'/api/v3/onezone/user/effective_spaces', oidc_token)
        if not result:
            logger.error("Obtaining list of spaces failed.")

        return result

    def get_space(self, oidc_token, space_id):
        # TODO it returns info about cached spaces without token verification!

        # Check the cache entries
        for cs in self.cached_spaces:
            if cs.id != space_id:
                continue

            # space_id found in cache
            if cs.expiration > datetime.now():
                # Entry still actual > return content
                return cs.object

            # Entry expired > remove from cache
            self.cached_spaces.remove(cs)
            break

        # Entry not found in cache or alredy expired
        result = self._make_request_get(f'/api/v3/onezone/spaces/{space_id}', oidc_token)
        if not result:
            logger.error(f"Obtaining info about space ID {space_id} failed.")

        # Save entry into the cache
        self.cached_spaces.append(
            self.CacheEntry(
                datetime.now() + timedelta(hours=1),
                space_id,
                result
            )
        )

        return result

    def get_provider(self, oidc_token, provider_id):
        # TODO it returns info about cached providers without token verification!

        # Check the cache entries
        for cs in self.cached_providers:
            if cs.id != provider_id:
                continue

            # provider_id found in cache
            if cs.expiration > datetime.now():
                # Entry still actual > return content
                return cs.object

            # Entry expired > remove from cache
            self.cached_providers.remove(cs)
            break

        # Entry not found in cache or alredy expired
        result = self._make_request_get(f'/api/v3/onezone/providers/{provider_id}', oidc_token)
        if not result:
            logger.error(f"Obtaining info about provider ID {provider_id} failed.")

        # Save entry into the cache
        self.cached_providers.append(
            self.CacheEntry(
                datetime.now() + timedelta(hours=1),
                provider_id,
                result
            )
        )

        return result
