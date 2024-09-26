import re
from collections import defaultdict

from helpers.url.url import parse_url
from helpers.html.fetch_html import fetch_html
from helpers.html.parse_html import parse_html

PROVIDER_LIST = [
    'Dealer.com', 'DealerInspire', 'DealerOn', 'DealerSocket', 'DealerFire',
    'DealereProcess', 'DealerSpike', 'DealerCloud', 'DealerCarSearch',
    'DealerCenter', 'Ansira', "Overfuel", 'V12 Software', 'Carsforsale.com',
    'Auto Corner', 'Fusion Zone', 'DealerWebsite.com', 'Vehicles Network',
    'Dealer Sync', 'Ebiz Autos', 'Auto Manager', 'Auto Revo', 'Fox Dealer',
    'Velocity', 'Liquid Motors', 'Remora', 'ASN Software', 'All Auto Network',
    'HomeNet', 'Speed Digital', 'Jazel Auto', 'Get My Auto', 'Surge Metrix',
    'Easy Cars', 'Dealer Front', 'Carbase', 'Car Story', '321 Ignition',
    'Sokall', 'Dealer Venom', 'Webtechs.net', 'Styleshout', 'Stocknum',
    'Sterling Emarketing', 'Promax', 'PRCO Power', 'Motorcar Marketing',
    'Motor Lot', 'Chroma Cars', 'Dealer Accelerate', 'Car Pro Live',
    'BG Develops', 'Auto Funds', 'Auto Click', 'Web4 Car Dealer',
    'Search Optics', 'Pixel Motion', 'Friday Systems', 'Dealer Vision',
    'Comply Auto', 'Carwizard.net', 'Auto Fusion'
]


def identify_dealer_provider(url):
    # Parse the URL and fetch the HTML content
    url = parse_url(url).netloc
    html = fetch_html(url)

    # Parse HTML content
    soup = parse_html(html)

    # Initialize a provider count dictionary using defaultdict for ease of updating counts
    provider_count = defaultdict(int)

    # Compile regex patterns for each provider just once
    provider_patterns = {provider: re.compile(
        provider, re.IGNORECASE) for provider in PROVIDER_LIST}

    # Search the text content and tag attributes for each provider pattern
    for tag in soup.find_all(True):  # True selects all tags
        # Search within the text
        if tag.string:
            for provider, pattern in provider_patterns.items():
                if pattern.search(tag.string):
                    provider_count[provider] += 1

        # Search within attributes
        for attr_value in tag.attrs.values():
            attr_str = ' '.join(attr_value) if isinstance(
                attr_value, list) else str(attr_value)
            for provider, pattern in provider_patterns.items():
                if pattern.search(attr_str):
                    provider_count[provider] += 1

    # Sort the provider_count dictionary by occurrences
    sorted_providers = sorted(provider_count.items(),
                              key=lambda item: item[1], reverse=True)

    # Return the top provider or None if no matches found
    if sorted_providers and sorted_providers[0][1] > 0:
        # Return the provider with the highest count
        return sorted_providers[0][0]
    return None
