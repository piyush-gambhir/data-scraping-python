from selenium import webdriver

from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options as ChromeOptions


def create_chrome_driver(headless=False, incognito=False):
    """
    Creates a Chrome WebDriver instance with custom options.

    Args:
    headless (bool): Run Chrome in headless mode (default: False).
    incognito (bool): Whether to run Chrome in incognito mode (default: False).

    Returns:
    WebDriver: The Selenium WebDriver instance for Chrome.
    """
    options = ChromeOptions()

    if headless:
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

    if incognito:
        options.add_argument('--incognito')

    return webdriver.Chrome(options=options)


def create_firefox_driver(headless=False, private_mode=False):
    """
    Creates a Firefox WebDriver instance with custom options.

    Args:
    headless (bool): Run Firefox in headless mode (default: False).
    private_mode (bool): Whether to run Firefox in private mode (default: False).

    Returns:
    WebDriver: The Selenium WebDriver instance for Firefox.
    """
    options = FirefoxOptions()

    if headless:
        options.add_argument('--headless')

    if private_mode:
        options.add_argument('--private')

    return webdriver.Firefox(options=options)


def create_edge_driver(headless=False, in_private=False):
    """
    Creates an Edge WebDriver instance with custom options.

    Args:
    headless (bool): Run Edge in headless mode (default: False).
    in_private (bool): Whether to run Edge in InPrivate mode (default: False).

    Returns:
    WebDriver: The Selenium WebDriver instance for Edge.
    """
    options = EdgeOptions()

    if headless:
        options.add_argument('headless')

    if in_private:
        options.add_argument('inprivate')

    return webdriver.Edge(options=options)
