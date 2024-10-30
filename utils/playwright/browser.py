import os

from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
from utils.logger.setup import setup_logger

logger = setup_logger(__name__)


async def launch_browser_async(
    headless=True, browser_type="chromium", args=["--no-sandbox", "--disable-gpu"]
):
    """
    Launches the browser using Playwright asynchronously.

    :param headless: Whether to run the browser in headless mode.
    :param browser_type: Browser type, e.g., 'chromium', 'firefox', or 'webkit'.
    :return: Browser instance and Playwright instance.
    """
    logger.info(
        f"Launching {browser_type} browser asynchronously (headless: {headless})"
    )
    playwright = await async_playwright().start()
    try:
        if browser_type == "chromium":
            browser = await playwright.chromium.launch(headless=headless, args=args)
            logger.info("Chromium browser launched successfully")
        elif browser_type == "firefox":
            browser = await playwright.firefox.launch(headless=headless, args=args)
            logger.info("Firefox browser launched successfully")
        elif browser_type == "webkit":
            browser = await playwright.webkit.launch(headless=headless, args=args)
            logger.info("Webkit browser launched successfully")
        else:
            logger.error(f"Invalid browser type: {browser_type}")
            raise ValueError(
                "Invalid browser type. Choose 'chromium', 'firefox', or 'webkit'."
            )

        return browser, playwright
    except Exception as e:
        logger.error(f"Error launching browser asynchronously: {str(e)}")
        raise


def launch_browser_sync(
    headless=True, browser_type="firefox", args=["--no-sandbox", "--disable-gpu"]
):
    """
    Launches the browser using Playwright synchronously.

    :param headless: Whether to run the browser in headless mode.
    :param browser_type: Browser type, e.g., 'chromium', 'firefox', or 'webkit'.
    :return: Browser instance and Playwright instance.
    """
    logger.info(
        f"Launching {browser_type} browser synchronously (headless: {headless})"
    )
    playwright = sync_playwright().start()
    try:
        if browser_type == "chromium":
            browser = playwright.chromium.launch(headless=headless, args=args)
            logger.info("Chromium browser launched successfully")
        elif browser_type == "firefox":
            browser = playwright.firefox.launch(
                headless=headless,
                args=args,
            )
            logger.info("Firefox browser launched successfully with custom profile")
        elif browser_type == "webkit":
            browser = playwright.webkit.launch(headless=headless, args=args)
            logger.info("Webkit browser launched successfully")
        else:
            logger.error(f"Invalid browser type: {browser_type}")
            raise ValueError(
                "Invalid browser type. Choose 'chromium', 'firefox', or 'webkit'."
            )

        return browser, playwright
    except Exception as e:
        logger.error(f"Error launching browser synchronously: {str(e)}")
        raise
