import requests
from requests.exceptions import RequestException, HTTPError
from utils.logger.setup import setup_logger

logger = setup_logger(__name__)


def fetch_html(url, headers=None, timeout=30, max_retries=3):
    """
    Fetches the HTML content of a web page with improved error handling and retries.

    Args:
    url (str): The URL of the page to scrape.
    headers (dict): Optional headers to send with the request.
    timeout (int): Timeout for the request in seconds. Default is 30.
    max_retries (int): Maximum number of retries for failed requests. Default is 3.

    Returns:
    tuple: (str, int) The HTML content of the page and the status code, or (None, None) on failure.
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, headers=headers, timeout=timeout)
            response.raise_for_status()
            return response.text, response.status_code
        except HTTPError as e:
            logger.warning(f"HTTP error occurred: {e}. Status code: {e.response.status_code}")
            return None, e.response.status_code
        except RequestException as e:
            logger.error(f"Error fetching {url} (Attempt {attempt + 1}/{max_retries}): {e}")
            if attempt == max_retries - 1:
                return None, None

    return None, None
