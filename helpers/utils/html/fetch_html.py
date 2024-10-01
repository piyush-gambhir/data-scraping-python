import requests


def fetch_html(url, headers=None):
    """
    Fetches the HTML content of a web page.

    Args:
    url (str): The URL of the page to scrape.
    headers (dict): Optional headers to send with the request.

    Returns:
    str: The HTML content of the page.
    """
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check if request was successful
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
