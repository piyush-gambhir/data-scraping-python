from utils.logger.setup import setup_logger
from selenium import webdriver
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.common.exceptions import WebDriverException
import time

logger = setup_logger(__name__)


def create_chrome_driver(headless=False, incognito=False):
    """
    Creates a Chrome WebDriver instance with custom options.

    Args:
    headless (bool): Run Chrome in headless mode (default: False).
    incognito (bool): Whether to run Chrome in incognito mode (default: False).

    Returns:
    WebDriver: The Selenium WebDriver instance for Chrome.
    """
    logger.info("Creating Chrome WebDriver")
    options = ChromeOptions()

    if headless:
        logger.info("Setting Chrome to headless mode")
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')

    if incognito:
        logger.info("Setting Chrome to incognito mode")
        options.add_argument('--incognito')

    try:
        driver = webdriver.Chrome(options=options)
        logger.info("Chrome WebDriver created successfully")
        return driver
    except WebDriverException as e:
        logger.error(f"Failed to create Chrome WebDriver: {str(e)}")
        raise


def create_firefox_driver(headless=False, private_mode=False):
    """
    Creates a Firefox WebDriver instance with custom options.

    Args:
    headless (bool): Run Firefox in headless mode (default: False).
    private_mode (bool): Whether to run Firefox in private mode (default: False).

    Returns:
    WebDriver: The Selenium WebDriver instance for Firefox.
    """
    logger.info("Creating Firefox WebDriver")
    options = FirefoxOptions()

    if headless:
        logger.info("Setting Firefox to headless mode")
        options.add_argument('--headless')

    if private_mode:
        logger.info("Setting Firefox to private mode")
        options.add_argument('--private')

    try:
        driver = webdriver.Firefox(options=options)
        logger.info("Firefox WebDriver created successfully")
        return driver
    except WebDriverException as e:
        logger.error(f"Failed to create Firefox WebDriver: {str(e)}")
        raise


def create_edge_driver(headless=False, in_private=False):
    """
    Creates an Edge WebDriver instance with custom options.

    Args:
    headless (bool): Run Edge in headless mode (default: False).
    in_private (bool): Whether to run Edge in InPrivate mode (default: False).

    Returns:
    WebDriver: The Selenium WebDriver instance for Edge.
    """
    logger.info("Creating Edge WebDriver")
    options = EdgeOptions()

    if headless:
        logger.info("Setting Edge to headless mode")
        options.add_argument('headless')

    if in_private:
        logger.info("Setting Edge to InPrivate mode")
        options.add_argument('inprivate')

    try:
        driver = webdriver.Edge(options=options)
        logger.info("Edge WebDriver created successfully")
        return driver
    except WebDriverException as e:
        logger.error(f"Failed to create Edge WebDriver: {str(e)}")
        raise


def restart_driver(driver, create_driver_func, **kwargs):
    """
    Restarts the WebDriver.

    Args:
    driver: The current WebDriver instance.
    create_driver_func: The function to create a new driver (e.g., create_chrome_driver).
    **kwargs: Additional arguments to pass to the create_driver_func.

    Returns:
    WebDriver: A new instance of the WebDriver.
    """
    logger.info("Restarting the WebDriver...")

    # Close the current driver
    if driver:
        driver.quit()

    # Create a new driver
    new_driver = create_driver_func(**kwargs)

    logger.info("WebDriver restarted successfully.")

    # Add a small delay to ensure the driver is fully initialized
    time.sleep(2)

    return new_driver
