import os
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import time
from selenium import webdriver
import subprocess
import requests
import xml.etree.ElementTree as ET


def setup_driver():
    driver = webdriver.Firefox()
    return driver


def fetch_html_content_using_selenium(url, sleep_time=30, percentage=1):
    driver = setup_driver()
    driver.get(url)
    time.sleep(sleep_time)
    content = driver.page_source
    driver.quit()
    content = content[:int(len(content) * percentage)]
    return BeautifulSoup(content, 'html.parser')


def fetch_html_content_using_requests(url, percentage=1):
    import requests
    response = requests.get(url)
    content = response.text
    content = content[:int(len(content) * percentage)]
    return BeautifulSoup(response, 'html.parser')


def fetch_sitemap_using_requests(url):
    response = requests.get(url)
    return response.text


def fetch_sitemap_using_selenium(url, sleep_time=30):
    driver = setup_driver()
    driver.get(url)
    time.sleep(sleep_time)
    response = driver.page_source
    driver.quit()
    return response


def parse_sitemap(sitemap_content):
    try:
        root = ET.fromstring(sitemap_content)
        return [elem.text for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    except Exception as e:
        soup = BeautifulSoup(sitemap_content, 'html.parser')
        links = soup.find_all('a')
        urls = [link.get('href') for link in links]
        return urls


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def is_valid_image_url(url):
    try:
        result = urlparse(url)
        if result.path.lower().endswith(('.png', '.svg', '.gif')):
            return False

        if 'logo' in result.path.lower():
            return False

        return all([result.scheme, result.netloc])
    except ValueError:
        return False


def get_website_base_url(url):
    parsed_uri = urlparse(url)
    return '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)


def download_image(image_url, save_path):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    try:
        response = requests.get(image_url, stream=True,
                                headers=headers, timeout=10)
        if response.status_code == 200:
            with open(save_path, 'wb') as out_file:
                out_file.write(response.content)
        else:
            pass
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while downloading {image_url}: {str(e)}")
