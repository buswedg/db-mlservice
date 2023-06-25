import logging
import requests
from django.conf import settings
from urllib.parse import urljoin

logger = logging.getLogger('custom')


class DBMLServiceHandler:
    """
    A module to handle DBMLService API related operations.
    """

    def __init__(self, user=None, password=None):
        self.BASE_URL = settings.DB_MLSERVICE_BASE_URL
        self.USER = user or settings.DB_MLSERVICE_USER
        self.PASSWORD = password or settings.DB_MLSERVICE_PASSWORD
        self.tokens = None

    def authenticate(self):
        data = {'username': self.USER, 'password': self.PASSWORD}
        endpoint = "token/"
        url = urljoin(self.BASE_URL, endpoint)

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            self.tokens = response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"DB ML Service: Failed to authenticate: {e}")

    def make_request(self, endpoint, method='GET', params=None, data=None):
        if not self.tokens:
            self.authenticate()

        bearer = "JWT " + self.tokens['access']
        headers = {
            'Content-type': 'application/json',
            'Authorization': bearer,
        }

        url = urljoin(self.BASE_URL, endpoint)

        try:
            response = requests.request(method, url, headers=headers, params=params, json=data)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"DB ML Service: Request failed: {e}")

    def get_endpoint(self, params=None):
        endpoint = "v1/endpoint/"
        return self.make_request(endpoint, method='GET', params=params)

    def get_ml_algorithm(self, params=None):
        endpoint = "v1/ml-algorithm/"
        return self.make_request(endpoint, method='GET', params=params)

    def get_ml_algorithm_request(self, params=None):
        endpoint = "v1/ml-algorithm-request/"
        return self.make_request(endpoint, method='GET', params=params)

    def get_ml_algorithm_status(self, params=None):
        endpoint = "v1/ml-algorithm-status/"
        return self.make_request(endpoint, method='GET', params=params)

    def update_ml_algorithm_status(self, data=None):
        endpoint = "v1/ml-algorithm-status/"
        return self.make_request(endpoint, method='POST', data=data)
