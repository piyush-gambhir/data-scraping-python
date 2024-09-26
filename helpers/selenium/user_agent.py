from selenium.webdriver.chrome.options import Options

def set_custom_user_agent(user_agent):
    """
    Sets a custom user agent for the browser.

    Args:
        user_agent (str): The custom user agent string.
    
    Returns:
        Options: ChromeOptions with the custom user agent.
    """
    chrome_options = Options()
    chrome_options.add_argument(f'user-agent={user_agent}')
    return chrome_options
