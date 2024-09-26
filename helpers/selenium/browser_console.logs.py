def get_browser_logs(driver):
    """
    Retrieves browser console logs.

    Args:
        driver (WebDriver): The Selenium WebDriver instance.

    Returns:
        list: A list of browser console log entries.
    """
    return driver.get_log('browser')
