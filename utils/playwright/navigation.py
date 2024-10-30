from utils.logger.setup import setup_logger

logger = setup_logger(__name__)


async def visit_url_async(browser, url, timeout=60000):
    """
    Opens a new page and navigates to the specified URL asynchronously with enhanced error handling and timeout.

    :param browser: The browser instance to use.
    :param url: The URL to navigate to.
    :param timeout: The maximum time to wait for navigation, in milliseconds. Defaults to 60 seconds.
    :return: The page object if successful, None otherwise.
    """
    try:
        # Open a new context and page
        context = await browser.new_context()
        page = await context.new_page()

        # Navigate to the URL with timeout
        response = await page.goto(url, timeout=timeout, wait_until="networkidle")

        # Check if the navigation was successful
        if response is None or not response.ok:
            logger.warning(f"Navigation to {url} failed or returned non-OK status.")
            return None

        logger.info(f"Successfully navigated to {url}")
        return page
    except Exception as e:
        logger.error(f"Error navigating to URL: {url}. Error: {str(e)}")
        # Close the page and context in case of an error
        if "page" in locals():
            await page.close()
        if "context" in locals():
            await context.close()
        return None


def visit_url_sync(browser, url, timeout=60000):
    """
    Opens a new page and navigates to the specified URL synchronously with enhanced error handling, timeout, and custom headers.

    :param browser: The browser instance to use.
    :param url: The URL to navigate to.
    :param timeout: The maximum time to wait for navigation, in milliseconds. Defaults to 60 seconds.
    :return: The page object if successful, None otherwise.
    """
    try:
        # Define custom headers to be used in the browser context
        custom_headers = {
            "Accept": "application/xhtml+xml, text/html, application/xml, */*; q=0.9,image/webp,image/apng, */*;",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
            "Connection": "keep-alive",
            "Referer": "https://www.google.com",
            "User-Agent": "PostmanRuntime/7.42.0",
        }

        # Open a new context with the custom headers
        context = browser.new_context(extra_http_headers=custom_headers)
        page = context.new_page()

        # Navigate to the URL with timeout
        response = page.goto(url, timeout=timeout, wait_until="load")

        # Check if the navigation was successful
        if response is None or not response.ok:
            logger.warning(f"Navigation to {url} failed or returned non-OK status.")
            return None

        logger.info(f"Successfully navigated to {url}")
        return page
    except Exception as e:
        logger.error(f"Error navigating to URL: {url}. Error: {str(e)}")
        # Close the page and context in case of an error
        if "page" in locals():
            page.close()
        if "context" in locals():
            context.close()
        return None
