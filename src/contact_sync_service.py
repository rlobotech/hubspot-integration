from src.hubspot_contact_handler import HubSpotContactHandler
from src.aws_contact_handler import AWSContactHandler
from utils.batch_processing import create_aws_batch_contacts
from config.logger import logger
from config.settings import MAX_WORKERS
from concurrent.futures import ThreadPoolExecutor, as_completed

class ContactSyncService:

    def __init__(self):
        self.aws_contact_handler = AWSContactHandler()
        self.hubspot_contact_handler = HubSpotContactHandler()

    def sync(self):
        aws_contacts = self.aws_contact_handler.fetch_contacts()
        if not aws_contacts:
            logger.info("No contacts to sync.")
            return

        batch_contacts = create_aws_batch_contacts(aws_contacts)

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            futures = {
                executor.submit(self.hubspot_contact_handler.upsert_contacts, batch): batch
                for batch in batch_contacts
            }
            for future in as_completed(futures):
                futures[future]
                try:
                    response = future.result()
                    if "error" in response:
                        logger.error(f"Error upserting contacts in HubSpot: {response['error']}")
                except Exception as e:
                    logger.error(f"Exception upserting contacts in HubSpot: {e}")
