import logging
import requests
from django.conf import settings
from urllib.parse import urljoin

logger = logging.getLogger('custom')


class DBTaxServiceHandler:
    """
    A module to handle DBTaxService API related operations.
    """

    def __init__(self, user=None, password=None):
        self.BASE_URL = settings.DB_TAXSERVICE_BASE_URL
        self.USER = user or settings.DB_TAXSERVICE_USER
        self.PASSWORD = password or settings.DB_TAXSERVICE_PASSWORD
        self.tokens = None

    def authenticate(self):
        data = {'username': self.USER, 'password': self.PASSWORD}

        endpoint = f"token/"
        url = urljoin(self.BASE_URL, endpoint)

        response = requests.post(url, data=data)

        if response.ok:
            self.tokens = response.json()
        else:
            logger.error(f"DB Tax Service: Failed to authenticate: {response.text}")
            self.tokens = None

    def get_tax_rate_by_postcode(self, zipcode):
        if not self.tokens:
            self.authenticate()

        if self.tokens is None:
            logger.error("DB Tax Service: Authentication failed. Unable to fetch tax rate.")
            return None

        bearer = "JWT " + self.tokens['access']
        headers = {
            'Content-type': 'application/json',
            'Authorization': bearer,
        }

        endpoint = f"tax/taxrate/bypostcode/?postcode={zipcode}"
        url = urljoin(self.BASE_URL, endpoint)

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            return response.json().get('estimated_combined_rate')
        except requests.exceptions.HTTPError as e:
            logger.error(f"DB Tax Service: Request failed: {e}")
        except requests.exceptions.RequestException as e:
            logger.error(f"DB Tax Service: Unexpected error occurred during request: {e}")

        return None