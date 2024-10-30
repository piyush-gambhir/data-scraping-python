from utils.logger.setup import setup_logger

logger = setup_logger(__name__)


async def take_screenshot_async(page, path='screenshot.png', full_page=True):
    """
    Takes a screenshot of the page asynchronously.
    """
    try:
        logger.info(f"Taking screenshot and saving to {path}")
        await page.screenshot(path=path, full_page=full_page)
        logger.info("Screenshot saved successfully")
    except Exception as e:
        logger.error(f"Error taking screenshot: {e}")
        raise e


def take_screenshot_sync(page, path='screenshot.png', full_page=True):
    """
    Takes a screenshot of the page synchronously.
    """
    try:
        logger.info(f"Taking screenshot and saving to {path}")
        page.screenshot(path=path, full_page=full_page)
        logger.info("Screenshot saved successfully")
    except Exception as e:
        logger.error(f"Error taking screenshot: {e}")
        raise e
