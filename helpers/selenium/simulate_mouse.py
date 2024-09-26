from selenium.webdriver.common.action_chains import ActionChains

def hover_over_element(driver, by, value, wait_time=10):
    """
    Hovers the mouse over an element.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        by (str): The type of selector (By.ID, By.XPATH, etc.)
        value (str): The selector value.
        wait_time (int): Time to wait for the element.
    """
    element = find_element(driver, by, value, wait_time)
    if element:
        actions = ActionChains(driver)
        actions.move_to_element(element).perform()
