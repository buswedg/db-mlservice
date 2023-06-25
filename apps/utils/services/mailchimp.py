import logging

import requests
from django.conf import settings

logger = logging.getLogger('custom')


class MailchimpHandler:
    """
    A module to handle Mailchimp API related operations.
    """

    def __init__(self, api_key=None):
        self.api_key = api_key or settings.MAILCHIMP_KEY
        self.client = requests.Session()
        self.client.auth = ('apikey', self.api_key)
        self.base_url = f"https://{self.api_key.split('-')[-1]}.api.mailchimp.com/3.0"

    def create_list(self, name, contact, permission_reminder, campaign_defaults, email_type_option):
        url = f"{self.base_url}/lists"
        data = {
            'name': name,
            'contact': contact,
            'permission_reminder': permission_reminder,
            'campaign_defaults': campaign_defaults,
            'email_type_option': email_type_option
        }

        try:
            response = self.client.post(url, json=data)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"MailChimp Service: Error creating list: {e}")

        return None

    def add_member_to_list(self, list_id, email_address):
        url = f"{self.base_url}/lists/{list_id}/members"
        data = {
            'email_address': email_address,
            'status': 'subscribed'
        }

        try:
            response = self.client.post(url, json=data)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"MailChimp Service: Error adding member to list: {e}")

        return None

    def delete_member_from_list(self, list_id, email_address):
        url = f"{self.base_url}/lists/{list_id}/members/{email_address}"

        try:
            response = self.client.delete(url)
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            logger.error(f"MailChimp Service: Error deleting member from list: {e}")

        return None
