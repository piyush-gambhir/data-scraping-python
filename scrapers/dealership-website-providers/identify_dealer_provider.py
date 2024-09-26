# installing dependencies
from concurrent.futures import ThreadPoolExecutor
from selenium import webdriver
import time
import re
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import subprocess

packages = ['requests', 'bs4', 'lxml', 'scrapy', 'selenium']
for package in packages:
    subprocess.call(['pip', 'install', package])


PROVIDER_LIST = [
    'Dealer.com',
    'DealerInspire',
    'DealerOn',
    'DealerSocket',
    'DealerFire',
    'DealereProcess',
    'DealerSpike',
    'DealerCloud',
    'DealerCarSearch',
    'DealerCenter',
    "Overfuel",
    'Ansira',
]

# %%


def setup_driver():
    """
    This function sets up the driver for the selenium
    """
    driver = webdriver.Firefox()
    return driver

# %%


def get_html_content(url):
    """
    This function gets the html content of the input url
    """
    driver = setup_driver()
    driver.get(url)
    time.sleep(5)
    html = driver.page_source
    driver.quit()

    return BeautifulSoup(html, 'lxml')


# %%


def identify_dealer_provider(url):
    """
    This function identifies the provider of the dealer website
    """
    soup = get_html_content(url)
    provider = None

    provider_count = {}
    for dealer_provider in PROVIDER_LIST:
        pattern = re.compile(dealer_provider, re.IGNORECASE)
        text_count = sum(1 for _ in soup.find_all(string=pattern))
        attrs_count = sum(1 for tag in soup.find_all(lambda tag: any(
            pattern.search(str(value)) for value in tag.attrs.values())))
        provider_count[dealer_provider] = text_count + attrs_count
    max_provider = max(provider_count, key=provider_count.get)
    if provider_count[max_provider] > 0:
        provider = max_provider

    return provider

# %%


def get_website_url(url):
    """
    This function gets the website url from the input url
    """
    parsed_uri = urlparse(url)
    domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
    return domain


# %%
def main(url):

    provider = identify_dealer_provider(url)
    print(provider)


if __name__ == "__main__":
    website_input_url = 'https://adosmotorsmn.com/vdp/21050525/Used-2012-Audi-Q5-20T-Premium-Plus-quattro-for-sale-in-Saint-Paul-MN-55102'
    main(website_input_url)
