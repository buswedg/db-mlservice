import logging
import requests
from django.conf import settings
from requests.auth import HTTPBasicAuth
from urllib.parse import urljoin

logger = logging.getLogger('custom')


class AvalaraHandler:
    """
    A module to handle Avalara API related operations.
    """

    def __init__(self, user=None, password=None):
        self.BASE_URL = settings.AVALARA_BASE_URL
        self.USER = user or settings.AVALARA_USER
        self.PASSWORD = password or settings.AVALARA_PASSWORD

    def get_tax_rate_by_postcode(self, zipcode, country='US'):
        headers = {
            'Content-Type': 'application/json'
        }

        endpoint = f"taxrates/bypostalcode?country={country}&postalCode={zipcode}"
        url = urljoin(self.BASE_URL, endpoint)

        try:
            response = requests.get(url, headers=headers, auth=HTTPBasicAuth(self.USER, self.PASSWORD))
            response.raise_for_status()
            return response.json().get('totalRate')
        except requests.exceptions.HTTPError as e:
            logger.error(f"Avalara Service: Request failed: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"Avalara Service: Unexpected error occurred during request: {e}")

        return None