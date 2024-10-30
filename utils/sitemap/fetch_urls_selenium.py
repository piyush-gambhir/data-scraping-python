from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

from utils.sitemap.type import identify_sitemap_type
from utils.logger.setup import setup_logger

logger = setup_logger(__name__)

# Selenium functions


def fetch_sitemap_urls_selenium(driver, sitemap_url):
    """
    Fetches all URLs from a given sitemap URL using Selenium based on its type.
    """
    urls = []
    try:
        logger.info(f"Fetching sitemap using Selenium from URL: {sitemap_url}")
        driver.get(sitemap_url)

        sitemap_type = identify_sitemap_type(driver.page_source)

        if sitemap_type == 'XML':
            urls = fetch_xml_sitemap_urls_selenium(driver)
        elif sitemap_type == 'HTML':
            urls = fetch_html_sitemap_urls_selenium(driver)
        elif sitemap_type == 'Text':
            urls = fetch_text_sitemap_urls_selenium(driver)
        elif sitemap_type == 'Sitemap Index':
            urls = fetch_sitemap_index_urls_selenium(driver)
        else:
            logger.warning(f"Unknown sitemap type for URL: {sitemap_url}")

        logger.info(f"Found {len(urls)} URLs in sitemap using Selenium")
    except Exception as e:
        logger.error(f"Error fetching sitemap with Selenium: {e}")
    return urls


def fetch_xml_sitemap_urls_selenium(driver):
    urls = []
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "loc")))
    loc_elements = driver.find_elements(By.TAG_NAME, "loc")
    for loc in loc_elements:
        url = loc.text.strip()
        if url.endswith('.xml'):
            logger.debug(f"Found nested sitemap: {url}")
            urls.extend(fetch_sitemap_urls_selenium(driver, url))
        else:
            urls.append(url)
    return urls


def fetch_html_sitemap_urls_selenium(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "a")))
    link_elements = driver.find_elements(By.TAG_NAME, "a")
    return [link.get_attribute('href') for link in link_elements if link.get_attribute('href') and link.get_attribute('href').startswith('http')]


def fetch_text_sitemap_urls_selenium(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "body")))
    body_text = driver.find_element(By.TAG_NAME, "body").text
    return [line.strip() for line in body_text.split('\n') if line.strip().startswith('http')]


def fetch_sitemap_index_urls_selenium(driver):
    urls = []
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.TAG_NAME, "loc")))
    loc_elements = driver.find_elements(By.TAG_NAME, "loc")
    for loc in loc_elements:
        url = loc.text.strip()
        urls.extend(fetch_sitemap_urls_selenium(driver, url))
    return urls

