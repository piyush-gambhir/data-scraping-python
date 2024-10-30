from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from utils.logger.setup import setup_logger
logger = setup_logger(__name__)


def fetch_html_selenium(driver, url, wait_time=10):
    """
    Navigates to the URL and fetches the HTML content.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        url (str): The URL to navigate to.
        wait_time (int): Time in seconds to wait for the page to load.

    Returns:
        str: The HTML content of the page, or None if an error occurs.

    Raises:
        TimeoutException: If the page fails to load within the specified wait time.
    """
    try:
        driver.get(url)
        WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )
        return driver.page_source
    except TimeoutException as e:
        logger.error(f"Timeout while waiting for page to load: {
                     url}. Error: {str(e)}")
        return None
    except Exception as e:
        logger.error(f"Unexpected error while fetching HTML from {
                     url}. Error: {str(e)}")
        return None


def find_element(driver, by, value, wait_time=10):
    """
    Finds an element on the page using various selectors.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        by (str): The type of selector (By.ID, By.CLASS_NAME, By.XPATH, etc.)
        value (str): The selector value.
        wait_time (int): Time in seconds to wait for the element.

    Returns:
        WebElement: The found WebElement, or None if not found.
    """
    try:
        return WebDriverWait(driver, wait_time).until(
            EC.presence_of_element_located((by, value))
        )
    except TimeoutException:
        print(f"Error: Element with selector {value} not found.")
        return None


def click_element(driver, by, value, wait_time=10):
    """
    Clicks on an element found by a specific selector.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        by (str): The type of selector (By.ID, By.CLASS_NAME, By.XPATH, etc.)
        value (str): The selector value.
        wait_time (int): Time in seconds to wait for the element.
    """
    element = find_element(driver, by, value, wait_time)
    if element:
        element.click()


def enter_text(driver, by, value, text, wait_time=10):
    """
    Enters text into a form input field.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        by (str): The type of selector (By.ID, By.NAME, By.XPATH, etc.)
        value (str): The selector value.
        text (str): The text to input.
        wait_time (int): Time in seconds to wait for the input field.
    """
    element = find_element(driver, by, value, wait_time)
    if element:
        element.clear()
        element.send_keys(text)


def scroll_to_element(driver, by, value, wait_time=10):
    """
    Scrolls the page to a specific element.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        by (str): The type of selector (By.ID, By.NAME, By.XPATH, etc.)
        value (str): The selector value.
        wait_time (int): Time in seconds to wait for the element.
    """
    element = find_element(driver, by, value, wait_time)
    if element:
        driver.execute_script("arguments[0].scrollIntoView();", element)


def wait_for_clickable(driver, by, value, wait_time=10):
    """
    Waits for an element to be clickable.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        by (str): The type of selector (By.ID, By.NAME, By.XPATH, etc.)
        value (str): The selector value.
        wait_time (int): Time in seconds to wait for the element.
    """
    try:
        element = WebDriverWait(driver, wait_time).until(
            EC.element_to_be_clickable((by, value))
        )
        return element
    except TimeoutException:
        print(f"Error: Element {value} not clickable.")
        return None


def select_dropdown_by_value(driver, by, value, option_value, wait_time=10):
    """
    Selects an option from a dropdown by its value.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        by (str): The type of selector (By.ID, By.NAME, By.XPATH, etc.)
        value (str): The selector value.
        option_value (str): The value of the option to select.
        wait_time (int): Time in seconds to wait for the dropdown.
    """
    element = find_element(driver, by, value, wait_time)
    if element:
        select = Select(element)
        select.select_by_value(option_value)


def take_screenshot(driver, file_name='screenshot.png'):
    """
    Takes a screenshot of the current page.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        file_name (str): The file name to save the screenshot as.
    """
    driver.save_screenshot(file_name)


def close_driver(driver):
    """
    Closes the WebDriver instance and browser.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
    """
    driver.quit()
