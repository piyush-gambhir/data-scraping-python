from playwright.async_api import Page
from utils.logger.setup import setup_logger

logger = setup_logger(__name__)

async def get_html_content(page: Page) -> str:
    """
    Retrieves the HTML content of the current page.
    :param page: Playwright Page object
    :return: HTML content as a string
    """
    try:
        logger.info("Fetching HTML content from the current page")
        html_content = await page.content()
        logger.info("Successfully retrieved HTML content")
        return html_content
    except Exception as e:
        logger.error(f"Error fetching HTML content: {str(e)}")
        raise

async def save_html_to_file(html_content: str, file_path: str) -> None:
    """
    Saves the HTML content to a file.
    :param html_content: HTML content as a string
    :param file_path: Path to save the HTML file
    """
    try:
        logger.info(f"Saving HTML content to file: {file_path}")
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_content)
        logger.info(f"HTML content successfully saved to {file_path}")
    except Exception as e:
        logger.error(f"Error saving HTML content to file: {str(e)}")
        raise

async def extract_element_text(page: Page, selector: str) -> str:
    """
    Extracts text from a specific element on the page.
    :param page: Playwright Page object
    :param selector: CSS selector for the target element
    :return: Text content of the element
    """
    try:
        logger.info(f"Extracting text from element with selector: {selector}")
        element = await page.query_selector(selector)
        if element:
            text = await element.inner_text()
            logger.info(f"Successfully extracted text: {text}")
            return text
        else:
            logger.warning(f"Element with selector {selector} not found")
            return ""
    except Exception as e:
        logger.error(f"Error extracting element text: {str(e)}")
        raise
