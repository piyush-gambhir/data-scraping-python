def open_new_tab(driver):
    """
    Opens a new browser tab and switches to it.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
    """
    driver.execute_script("window.open('');")
    driver.switch_to.window(driver.window_handles[-1])

def close_current_tab(driver):
    """
    Closes the current browser tab or window and switches to the previous one.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
    """
    driver.close()
    driver.switch_to.window(driver.window_handles[-1])
