import requests
from bs4 import BeautifulSoup

from utils.sitemap.type import identify_sitemap_type
from utils.logger.setup import setup_logger
logger = setup_logger(__name__)

# Requests function


def fetch_sitemap_urls_requests(sitemap_url):
    """
    Fetches all URLs from a given sitemap URL using requests based on its type.
    """
    urls = []
    try:
        logger.info(f"Fetching sitemap using requests from URL: {sitemap_url}")
        response = requests.get(sitemap_url)
        response.raise_for_status()

        sitemap_type = identify_sitemap_type(response.text)

        if sitemap_type == 'XML':
            urls = fetch_xml_sitemap_urls_requests(response.text)
        elif sitemap_type == 'HTML':
            urls = fetch_html_sitemap_urls_requests(response.text)
        elif sitemap_type == 'Text':
            urls = fetch_text_sitemap_urls_requests(response.text)
        elif sitemap_type == 'Sitemap Index':
            urls = fetch_sitemap_index_urls_requests(response.text)
        else:
            logger.warning(f"Unknown sitemap type for URL: {sitemap_url}")

        logger.info(f"Found {len(urls)} URLs in sitemap using requests")
    except Exception as e:
        logger.error(f"Error fetching sitemap with requests: {e}")
    return urls


def fetch_xml_sitemap_urls_requests(content):
    soup = BeautifulSoup(content, 'xml')
    urls = []
    for loc in soup.find_all('loc'):
        url = loc.text.strip()
        if url.endswith('.xml'):
            logger.debug(f"Found nested sitemap: {url}")
            urls.extend(fetch_sitemap_urls_requests(url))
        else:
            urls.append(url)
    return urls


def fetch_html_sitemap_urls_requests(content):
    soup = BeautifulSoup(content, 'html.parser')
    return [a['href'] for a in soup.find_all('a', href=True) if a['href'].startswith('http')]


def fetch_text_sitemap_urls_requests(content):
    return [line.strip() for line in content.split('\n') if line.strip().startswith('http')]


def fetch_sitemap_index_urls_requests(content):
    soup = BeautifulSoup(content, 'xml')
    urls = []
    for loc in soup.find_all('loc'):
        url = loc.text.strip()
        urls.extend(fetch_sitemap_urls_requests(url))
    return urls
