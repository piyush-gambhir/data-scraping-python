from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
from collections import deque

from utils.logger.setup import setup_logger
from utils.sitemap.type import identify_sitemap_type
from utils.playwright.navigation import visit_url_sync

logger = setup_logger(__name__)


def fetch_sitemap_urls_playwright(browser, sitemap_url, visited=None, max_depth=10):
    """
    Extracts all URLs from a given sitemap URL using Playwright, including nested sitemaps.
    Implements visited tracking and maximum recursion depth to prevent infinite loops.

    Args:
        browser: Playwright browser instance.
        sitemap_url (str): The URL of the sitemap to parse.
        visited (set, optional): Set of already visited sitemap URLs. Defaults to None.
        max_depth (int, optional): Maximum depth for nested sitemaps. Defaults to 10.

    Returns:
        tuple: (sitemap_accessibility (bool), sitemap_accessibility_message (str),
                sitemap_urls (list), sitemap_type (str))
    """
    if visited is None:
        visited = set()
    sitemap_urls = []
    sitemap_type = "Unknown"
    sitemap_accessibility = False
    sitemap_accessibility_message = ""

    # Initialize a queue with the initial sitemap URL and its depth
    queue = deque()
    queue.append((sitemap_url, 0))

    try:
        while queue:
            current_sitemap, depth = queue.popleft()
            if current_sitemap in visited:
                logger.debug(f"Already visited sitemap: {current_sitemap}. Skipping.")
                continue
            if depth > max_depth:
                logger.warning(f"Maximum sitemap nesting depth reached at: {current_sitemap}. Skipping further nesting.")
                continue

            visited.add(current_sitemap)
            logger.info(f"Fetching sitemap using Playwright from URL: {current_sitemap} at depth {depth}")
            try:
                page = visit_url_sync(browser, current_sitemap)
                sitemap_content = page.content()
            except Exception as fetch_error:
                logger.error(f"Error fetching sitemap {current_sitemap}: {str(fetch_error)}")
                sitemap_accessibility_message += f"Error fetching sitemap {current_sitemap}: {str(fetch_error)}\n"
                continue

            if sitemap_content:
                sitemap_accessibility = True
                sitemap_accessibility_message += f"Sitemap accessed successfully: {current_sitemap}\n"
                sitemap_type = identify_sitemap_type(sitemap_content)

                if sitemap_type in ['XML', 'Sitemap Index']:
                    try:
                        root = ET.fromstring(sitemap_content)
                        namespaces = {
                            'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
                        loc_elements = root.findall('.//ns:loc', namespaces)
                        extracted_urls = [loc.text.strip()
                                          for loc in loc_elements if loc.text]
                        logger.debug(f"Found {len(extracted_urls)} URLs in XML sitemap: {current_sitemap}")
                    except ET.ParseError as parse_error:
                        logger.error(f"XML parsing error for sitemap {current_sitemap}: {str(parse_error)}")
                        sitemap_accessibility_message += f"XML parsing error for sitemap {current_sitemap}: {str(parse_error)}\n"
                        continue

                elif sitemap_type == 'HTML':
                    try:
                        soup = BeautifulSoup(sitemap_content, 'html.parser')
                        extracted_urls = [link['href'].strip() for link in soup.find_all(
                            'a', href=True) if link['href'].startswith('http')]
                        logger.debug(f"Found {len(extracted_urls)} URLs in HTML sitemap: {current_sitemap}")
                    except Exception as parse_error:
                        logger.error(f"HTML parsing error for sitemap {current_sitemap}: {str(parse_error)}")
                        sitemap_accessibility_message += f"HTML parsing error for sitemap {current_sitemap}: {str(parse_error)}\n"
                        continue

                elif sitemap_type == 'Text':
                    try:
                        extracted_urls = [line.strip() for line in sitemap_content.split(
                            '\n') if line.strip().startswith('http')]
                        logger.debug(f"Found {len(extracted_urls)} URLs in Text sitemap: {current_sitemap}")
                    except Exception as parse_error:
                        logger.error(f"Text parsing error for sitemap {current_sitemap}: {str(parse_error)}")
                        sitemap_accessibility_message += f"Text parsing error for sitemap {current_sitemap}: {str(parse_error)}\n"
                        continue
                else:
                    logger.warning(f"Unknown sitemap type for URL: {current_sitemap}")
                    sitemap_accessibility_message += f"Unknown sitemap type for URL: {current_sitemap}\n"
                    extracted_urls = []

                for url in extracted_urls:
                    if url.endswith('.xml') or 'sitemap' in url.lower():
                        queue.append((url, depth + 1))
                    else:
                        sitemap_urls.append(url)
            else:
                logger.warning(f"Failed to fetch sitemap: HTTP {page.status}")
                sitemap_accessibility_message += f"Failed to fetch sitemap {current_sitemap}: HTTP {page.status}\n"
        
    except Exception as e:
        sitemap_accessibility_message += f"Error fetching sitemap with Playwright: {str(e)}\n"
        logger.error(f"Error fetching sitemap with Playwright: {str(e)}")

    logger.info(f"Extracted {len(sitemap_urls)} URLs from sitemap(s): {sitemap_url}")
    return sitemap_accessibility, sitemap_accessibility_message, sitemap_urls, sitemap_type
