def manage_cookies(driver, action='get', cookie=None):
    """
    Manages browser cookies (add, get, delete).

    Args:
        driver (WebDriver): The Selenium WebDriver instance.
        action (str): The action to take ('get', 'add', 'delete').
        cookie (dict): The cookie to add (only required for 'add' action).

    Returns:
        dict: The cookie information if 'get', or None if 'add' or 'delete'.
    """
    if action == 'get':
        return driver.get_cookies()
    elif action == 'add' and cookie:
        driver.add_cookie(cookie)
    elif action == 'delete':
        driver.delete_all_cookies()
    else:
        print("Invalid action or missing cookie for 'add' action.")
        return None
