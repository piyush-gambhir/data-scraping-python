import requests
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helpers.utils.selenium.webdriver import create_firefox_driver


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


def fetch_sitemap_urls_selenium(sitemap_url):
    """
    Fetches all URLs from a given sitemap XML URL using Selenium. Handles nested sitemaps as well.

    Args:
        sitemap_url (str): The URL of the sitemap.

    Returns:
        list: A list of URLs found in the sitemap.
    """

    urls = []

    try:
        # Initialize the WebDriver (you may need to specify the path to your driver)
        driver = create_firefox_driver(
            headless=True,
            private_mode=True
        )

        # Navigate to the sitemap URL
        driver.get(sitemap_url)

        # Wait for the page to load and the <loc> elements to be present
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.TAG_NAME, "loc"))
        )

        # Find all <loc> elements
        loc_elements = driver.find_elements(By.TAG_NAME, "loc")

        for loc in loc_elements:
            url = loc.text.strip()

            # Check if it's a sitemap (nested sitemaps)
            if url.endswith('.xml'):
                # Recursively fetch URLs from the nested sitemap
                urls.extend(fetch_sitemap_urls_selenium(url))
            else:
                urls.append(url)

    except Exception as e:
        print(f"Error fetching sitemap with Selenium: {e}")

    finally:
        # Close the browser
        driver.quit()

    return urls


# if __name__ == "__main__":
#     sitemap_url = "https://www.hendrickhonda.com/sitemap.xml"
#     urls = fetch_sitemap_urls_selenium(sitemap_url)

#     print(f"Total URLs found: {len(urls)}")
#     for url in urls:
#         print(url)
