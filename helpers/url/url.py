from urllib.parse import urlparse, urlunparse, urlencode, parse_qs, urljoin, quote, unquote


def construct_url(scheme='https', netloc='', path='', query_params=None, fragment=''):
    """
    Constructs a URL from its components.

    Args:
    scheme (str): The URL scheme (e.g., 'http', 'https').
    netloc (str): The network location (domain name, e.g., 'example.com').
    path (str): The path of the resource (e.g., '/path/to/resource').
    query_params (dict): A dictionary of query parameters (e.g., {'key': 'value'}).
    fragment (str): The fragment (e.g., 'section1').

    Returns:
    str: The constructed URL.
    """
    if query_params:
        query_string = urlencode(query_params)
    else:
        query_string = ''

    url = urlunparse((scheme, netloc, path, '', query_string, fragment))
    return url


def parse_url(url):
    """
    Parses a URL and returns its components.

    Args:
    url (str): The URL to parse.

    Returns:
    dict: A dictionary with the URL's components.
    """
    parsed_url = urlparse(url)
    # Parse the query string into a dict
    query_params = parse_qs(parsed_url.query)
    return {
        'scheme': parsed_url.scheme,
        'netloc': parsed_url.netloc,
        'path': parsed_url.path,
        'query_params': query_params,
        'fragment': parsed_url.fragment,
    }


def add_query_params(url, params):
    """
    Adds or updates query parameters in a URL.

    Args:
    url (str): The original URL.
    params (dict): A dictionary of query parameters to add or update.

    Returns:
    str: The updated URL with added query parameters.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)
    query_params.update(params)  # Update or add new query parameters
    query_string = urlencode(query_params, doseq=True)

    return urlunparse(parsed_url._replace(query=query_string))


def remove_query_params(url, params_to_remove):
    """
    Removes specific query parameters from a URL.

    Args:
    url (str): The original URL.
    params_to_remove (list): A list of query parameters to remove.

    Returns:
    str: The updated URL without the specified query parameters.
    """
    parsed_url = urlparse(url)
    query_params = parse_qs(parsed_url.query)

    for param in params_to_remove:
        query_params.pop(param, None)  # Remove the specified query parameters

    query_string = urlencode(query_params, doseq=True)

    return urlunparse(parsed_url._replace(query=query_string))


def join_url(base_url, relative_path):
    """
    Joins a base URL with a relative path to form a full URL.

    Args:
    base_url (str): The base URL.
    relative_path (str): The relative path to add to the base URL.

    Returns:
    str: The joined URL.
    """
    return urljoin(base_url, relative_path)


def encode_url_component(component):
    """
    Encodes a URL component (e.g., a query parameter or path segment).

    Args:
    component (str): The component to encode.

    Returns:
    str: The encoded component.
    """
    return quote(component)


def decode_url_component(component):
    """
    Decodes an encoded URL component.

    Args:
    component (str): The encoded component to decode.

    Returns:
    str: The decoded component.
    """
    return unquote(component)
