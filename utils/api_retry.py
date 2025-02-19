import time

from hubspot.crm.contacts.exceptions import ApiException
from config.logger import logger
from config.settings import HUBSPOT_CLIENT_MAX_RETRIES, HUBSPOT_CLIENT_BACKOFF_FACTOR

def retry_on_rate_limit_and_timeout(func):
    def wrapper(*args, **kwargs):
        for attempt in range(HUBSPOT_CLIENT_MAX_RETRIES):
            try:
                return func(*args, **kwargs)
            except ApiException as e:
                if e.status in {429, 500, 502, 504}:
                    wait_time = HUBSPOT_CLIENT_BACKOFF_FACTOR * (2 ** attempt)
                    logger.warning(f"API Error {e.status}. Retrying in {wait_time:.2f} seconds... (Attempt {attempt + 1}/{HUBSPOT_CLIENT_MAX_RETRIES})")
                    time.sleep(wait_time)
                else:
                    logger.error(f"API Exception: {e}")
                    return {"error": str(e)}
        return {"error": "Max retries reached. Failed to process request."}
    return wrapper
