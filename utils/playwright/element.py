from utils.logger.setup import setup_logger

logger = setup_logger(__name__)

def wait_for_element(page, selector, timeout=30000):
    """
    Wait for an element to appear on the page.
    """
    try:
        logger.info(f"Waiting for element with selector: {selector}")
        element = page.wait_for_selector(selector, timeout=timeout)
        logger.info(f"Element found: {selector}")
        return element
    except Exception as e:
        logger.error(f"Error: Element {selector} not found within {timeout} ms")
        raise e

def extract_text(page, selector):
    """
    Extracts text from a page element using its selector.
    """
    try:
        logger.info(f"Extracting text from element with selector: {selector}")
        element = page.query_selector(selector)
        if element:
            text = element.inner_text()
            logger.info(f"Text extracted: {text}")
            return text
        else:
            logger.warning(f"Element not found for selector: {selector}")
            raise ValueError(f"Element not found for selector: {selector}")
    except Exception as e:
        logger.error(f"Error extracting text: {e}")
        return None

def click_element(page, selector):
    """
    Clicks an element using the given selector.
    """
    try:
        logger.info(f"Clicking element with selector: {selector}")
        page.click(selector)
        logger.info(f"Element clicked: {selector}")
    except Exception as e:
        logger.error(f"Error clicking element {selector}: {e}")
        raise e

def fill_form_field(page, selector, value):
    """
    Fills a form field with the specified value.
    """
    try:
        logger.info(f"Filling form field with selector: {selector}")
        page.fill(selector, value)
        logger.info(f"Form field filled: {selector}")
    except Exception as e:
        logger.error(f"Error filling form field {selector}: {e}")
        raise e
