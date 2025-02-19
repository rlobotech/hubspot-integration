import requests

from config.logger import logger
from config.settings import AWS_ACCESS_KEY, AWS_PROD_URL
from requests.exceptions import RequestException

class AWSContactHandler:

    CONTACTS_ENDPOINT = "/contacts"
    REQUEST_TIMEOUT = 10

    def __init__(self):
        self.api_url = AWS_PROD_URL + self.CONTACTS_ENDPOINT
        self.bearer_token = AWS_ACCESS_KEY

    def fetch_contacts(self):
        headers = {"Authorization": f"Bearer {self.bearer_token}"}
        try:
            response = requests.get(self.api_url, headers=headers, timeout=self.REQUEST_TIMEOUT)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            logger.error(f"Error fetching contacts from AWS: {e}")
            return []
