import re
from collections import defaultdict

from helpers.url.url import parse_url
from helpers.html.fetch_html import fetch_html
from helpers.html.parse_html import parse_html

PROVIDER_LIST = [
    'Dealer.com', 'DealerInspire', 'DealerOn', 'DealerSocket', 'DealerFire',
    'DealereProcess', 'DealerSpike', 'DealerCloud', 'DealerCarSearch',
    'DealerCenter', 'Ansira', 'Overfuel', 'V12 Software', 'Carsforsale.com',
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

# Map each provider name to more flexible regex patterns
SPECIFIC_PATTERNS = {
    'Dealer.com': re.compile(r'dealer\.com', re.IGNORECASE),
    'DealerInspire': re.compile(r'dealer[\W_]*inspire', re.IGNORECASE),
    'DealerOn': re.compile(r'dealer[\W_]*on', re.IGNORECASE),
    'DealerSocket': re.compile(r'dealer[\W_]*socket', re.IGNORECASE),
    'DealerFire': re.compile(r'dealer[\W_]*fire', re.IGNORECASE),
    'DealereProcess': re.compile(r'dealer[\W_]*e[\W_]*process', re.IGNORECASE),
    'DealerSpike': re.compile(r'dealer[\W_]*spike', re.IGNORECASE),
    'DealerCloud': re.compile(r'dealer[\W_]*cloud', re.IGNORECASE),
    'DealerCarSearch': re.compile(r'dealer[\W_]*car[\W_]*search', re.IGNORECASE),
    'DealerCenter': re.compile(r'dealer[\W_]*center', re.IGNORECASE),
    'Ansira': re.compile(r'ansira[\W_]*(\.net)?', re.IGNORECASE),
    'Overfuel': re.compile(r'overfuel', re.IGNORECASE),
    'V12 Software': re.compile(r'v12[\W_]*software', re.IGNORECASE),
    'Carsforsale.com': re.compile(r'carsforsale\.com', re.IGNORECASE),
    'Auto Corner': re.compile(r'auto[\W_]*corner', re.IGNORECASE),
    'Fusion Zone': re.compile(r'fusion[\W_]*zone', re.IGNORECASE),
    'DealerWebsite.com': re.compile(r'dealerwebsite\.com', re.IGNORECASE),
    'Vehicles Network': re.compile(r'vehicles[\W_]*network', re.IGNORECASE),
    'Dealer Sync': re.compile(r'dealer[\W_]*sync', re.IGNORECASE),
    'Ebiz Autos': re.compile(r'ebiz[\W_]*autos', re.IGNORECASE),
    'Auto Manager': re.compile(r'auto[\W_]*manager', re.IGNORECASE),
    'Auto Revo': re.compile(r'auto[\W_]*revo', re.IGNORECASE),
    'Fox Dealer': re.compile(r'fox[\W_]*dealer', re.IGNORECASE),
    'Velocity': re.compile(r'velocity', re.IGNORECASE),
    'Liquid Motors': re.compile(r'liquid[\W_]*motors', re.IGNORECASE),
    'Remora': re.compile(r'remora', re.IGNORECASE),
    'ASN Software': re.compile(r'asn[\W_]*software', re.IGNORECASE),
    'All Auto Network': re.compile(r'all[\W_]*auto[\W_]*network', re.IGNORECASE),
    'HomeNet': re.compile(r'homenet', re.IGNORECASE),
    'Speed Digital': re.compile(r'speed[\W_]*digital', re.IGNORECASE),
    'Jazel Auto': re.compile(r'jazel[\W_]*auto', re.IGNORECASE),
    'Get My Auto': re.compile(r'get[\W_]*my[\W_]*auto', re.IGNORECASE),
    'Surge Metrix': re.compile(r'surge[\W_]*metrix', re.IGNORECASE),
    'Easy Cars': re.compile(r'easy[\W_]*cars', re.IGNORECASE),
    'Dealer Front': re.compile(r'dealer[\W_]*front', re.IGNORECASE),
    'Carbase': re.compile(r'carbase', re.IGNORECASE),
    'Car Story': re.compile(r'car[\W_]*story', re.IGNORECASE),
    '321 Ignition': re.compile(r'321[\W_]*ignition', re.IGNORECASE),
    'Sokall': re.compile(r'sokall', re.IGNORECASE),
    'Dealer Venom': re.compile(r'dealer[\W_]*venom', re.IGNORECASE),
    'Webtechs.net': re.compile(r'webtechs\.net', re.IGNORECASE),
    'Styleshout': re.compile(r'styleshout', re.IGNORECASE),
    'Stocknum': re.compile(r'stocknum', re.IGNORECASE),
    'Sterling Emarketing': re.compile(r'sterling[\W_]*emarketing', re.IGNORECASE),
    'Promax': re.compile(r'promax', re.IGNORECASE),
    'PRCO Power': re.compile(r'prco[\W_]*power', re.IGNORECASE),
    'Motorcar Marketing': re.compile(r'motorcar[\W_]*marketing', re.IGNORECASE),
    'Motor Lot': re.compile(r'motor[\W_]*lot', re.IGNORECASE),
    'Chroma Cars': re.compile(r'chroma[\W_]*cars', re.IGNORECASE),
    'Dealer Accelerate': re.compile(r'dealer[\W_]*accelerate', re.IGNORECASE),
    'Car Pro Live': re.compile(r'car[\W_]*pro[\W_]*live', re.IGNORECASE),
    'BG Develops': re.compile(r'bg[\W_]*develops', re.IGNORECASE),
    'Auto Funds': re.compile(r'auto[\W_]*funds', re.IGNORECASE),
    'Auto Click': re.compile(r'auto[\W_]*click', re.IGNORECASE),
    'Web4 Car Dealer': re.compile(r'web4[\W_]*car[\W_]*dealer', re.IGNORECASE),
    'Search Optics': re.compile(r'search[\W_]*optics', re.IGNORECASE),
    'Pixel Motion': re.compile(r'pixel[\W_]*motion', re.IGNORECASE),
    'Friday Systems': re.compile(r'friday[\W_]*systems', re.IGNORECASE),
    'Dealer Vision': re.compile(r'dealer[\W_]*vision', re.IGNORECASE),
    'Comply Auto': re.compile(r'comply[\W_]*auto', re.IGNORECASE),
    'Carwizard.net': re.compile(r'carwizard\.net', re.IGNORECASE),
    'Auto Fusion': re.compile(r'auto[\W_]*fusion', re.IGNORECASE),
}


def identify_dealer_provider(url):

    parsed_url_dict = parse_url(url)
    parsed_url = f"{parsed_url_dict['scheme']}://{parsed_url_dict['netloc']}"

    # Fetch the HTML content
    html = fetch_html(parsed_url)
    # Parse HTML content
    soup = parse_html(html)

    # Initialize a provider count dictionary using defaultdict for ease of updating counts
    provider_count = defaultdict(int)

    # Search the text content and tag attributes for each provider pattern
    for tag in soup.find_all(True):  # True selects all tags
        # Search within the text
        if tag.string:
            text_content = tag.string
            # Check specific patterns first
            for provider, pattern in SPECIFIC_PATTERNS.items():
                if pattern.search(text_content):
                    provider_count[provider] += 1

        # Search within attributes
        for attr_value in tag.attrs.values():
            attr_str = ' '.join(attr_value) if isinstance(
                attr_value, list) else str(attr_value)
            # Check specific patterns first
            for provider, pattern in SPECIFIC_PATTERNS.items():
                if pattern.search(attr_str):
                    provider_count[provider] += 1

    # Sort the provider_count dictionary by occurrences
    sorted_providers = sorted(provider_count.items(),
                              key=lambda item: item[1], reverse=True)

    # Return the top provider or None if no matches found
    if sorted_providers and sorted_providers[0][1] > 0:
        return sorted_providers[0][0]
    else:
        return None
