from hubspot import HubSpot
from utils.api_retry import retry_on_rate_limit_and_timeout
from utils.batch_processing import create_hubspot_batch_input
from config.settings import HUBSPOT_API_KEY
from config.logger import logger

class HubSpotContactHandler:

    def __init__(self):
        # Tried to apply the following retry but it did not work as expected.
        # retry = Retry(
        #     total = HUBSPOT_CLIENT_MAX_RETRIES,
        #     backoff_factor = HUBSPOT_CLIENT_BACKOFF_FACTOR,
        #     status_forcelist = (429, 500, 502, 504)
        # )
        self.client = HubSpot()
        self.client.access_token = HUBSPOT_API_KEY

    @retry_on_rate_limit_and_timeout
    def upsert_contacts(self, contacts):
        batch_input = create_hubspot_batch_input(contacts)
        api_response = self.client.crm.contacts.batch_api.upsert(batch_input)
        logger.info(f"Successfully upserted {len(batch_input.inputs)} contacts in HubSpot.")
        return api_response.to_dict()
