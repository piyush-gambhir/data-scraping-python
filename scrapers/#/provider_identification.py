import re
from web_scraping import fetch_html_content_using_requests, fetch_html_content_using_selenium, get_website_base_url

PROVIDER_LIST = [
    'Dealer.com', 'DealerInspire', 'DealerOn', 'DealerSocket', 'DealerFire',
    'DealereProcess', 'DealerSpike', 'DealerCloud', 'DealerCarSearch',
    'DealerCenter', 'Ansira', "Overfuel",
]


def identify_dealer_provider(url):
    url = get_website_base_url(url)
    soup = fetch_html_content_using_requests(url)
    provider_count = {}
    for dealer_provider in PROVIDER_LIST:
        pattern = re.compile(dealer_provider, re.IGNORECASE)
        text_count = sum(1 for _ in soup.find_all(string=pattern))
        attrs_count = sum(1 for tag in soup.find_all(lambda tag: any(
            pattern.search(str(value)) for value in tag.attrs.values())))
        provider_count[dealer_provider] = text_count + attrs_count
    max_provider = max(provider_count, key=provider_count.get)
    return max_provider if provider_count[max_provider] > 0 else None
