import requests
from bs4 import BeautifulSoup


def fetch_sitemap_urls(sitemap_url):
    """
    Fetches all URLs from a given sitemap XML URL. Handles nested sitemaps as well.

    Args:
        sitemap_url (str): The URL of the sitemap.

    Returns:
        list: A list of URLs found in the sitemap.
    """
    urls = []

    try:
        # Send a request to fetch the sitemap content
        response = requests.get(sitemap_url)

        # Raise an exception for bad status codes
        response.raise_for_status()

        # Parse the sitemap XML using BeautifulSoup
        soup = BeautifulSoup(response.content, 'xml')

        # Find all <loc> tags, which contain the URLs in the sitemap
        loc_tags = soup.find_all('loc')

        for loc in loc_tags:
            url = loc.text.strip()

            # Check if it's a sitemap (nested sitemaps)
            if url.endswith('.xml'):
                # Recursively fetch URLs from the nested sitemap
                urls.extend(fetch_sitemap_urls(url))
            else:
                urls.append(url)

    except requests.exceptions.RequestException as e:
        print(f"Error fetching sitemap: {e}")

    return urls
