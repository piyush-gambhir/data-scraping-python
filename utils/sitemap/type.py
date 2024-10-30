from utils.logger.setup import setup_logger
from utils.url.url import parse_url

logger = setup_logger(__name__)


def identify_sitemap_type(sitemap_content):
    """
    Identifies the type of sitemap based on the provided content.

    Args:
        sitemap_content (str): The content of the sitemap.

    Returns:
        str: The identified sitemap type ('XML', 'HTML', 'Text', 'Sitemap Index', or 'Unknown').
    """
    try:
        logger.info("Identifying sitemap type")

        # Check if it's an XML sitemap

        if 'urlset' in sitemap_content:
            logger.info("Identified XML sitemap")
            return 'XML'
        elif sitemap_content.strip().startswith('<?xml') and 'sitemapindex' in sitemap_content:
            logger.info("Identified Sitemap Index")
            return 'Sitemap Index'

        # Check if it's an HTML sitemap
        if sitemap_content.strip().startswith('<!DOCTYPE html') or '<html' in sitemap_content:
            logger.info("Identified HTML sitemap")
            return 'HTML'

        # Check if it's a text sitemap (one URL per line)
        lines = sitemap_content.strip().split('\n')
        if all(parse_url(line.strip()).get('scheme') for line in lines):
            logger.info("Identified Text sitemap")
            return 'Text'

        # If we can't determine the type, return Unknown
        logger.warning("Unable to identify sitemap type")
        return 'Unknown'

    except Exception as e:
        logger.error(f"Error identifying sitemap type: {e}")
        return 'Unknown'
