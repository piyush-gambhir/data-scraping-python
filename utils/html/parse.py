from bs4 import BeautifulSoup


def parse_html(html_content):
    """
    Parses the HTML content using BeautifulSoup.

    Args:
    html_content (str): The HTML content to parse.

    Returns:
    BeautifulSoup: A BeautifulSoup object for HTML parsing.
    """
    if html_content:
        return BeautifulSoup(html_content, 'html.parser')
    else:
        print("Empty HTML content provided.")
        return None
