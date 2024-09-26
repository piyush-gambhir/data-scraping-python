from selenium.webdriver.common.keys import Keys


def send_keypress(driver, by, value, key=Keys.ENTER, wait_time=10):
    """
    Sends a keypress to an element.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        by (str): The type of selector (By.ID, By.XPATH, etc.)
        value (str): The selector value.
        key (str): The key to send (e.g., Keys.ENTER, Keys.TAB).
        wait_time (int): Time to wait for the element.
    """
    element = find_element(driver, by, value, wait_time)
    if element:
        element.send_keys(key)
