import re
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urlparse

from helpers.utils.html.fetch_html import fetch_html
from helpers.utils.html.parse_html import parse_html



def extract_vin(soup):
    """Extract VIN number from the HTML soup."""
    vin_pattern = re.compile(r'[A-HJ-NPR-Z0-9]{17}')  # Pattern for a 17-character VIN
    for text in soup.stripped_strings:
        match = vin_pattern.search(text)
        if match:
            return match.group()
    return None

def extract_images(soup):
    """Extract image URLs from the HTML soup."""
    images = set()
    for section in soup.find_all('section', id=re.compile(r'vdp-photos-dealershipPhotoGallery.*')):
        for img in section.find_all('img'):
            src = img.get('src')
            if src and src.lower().endswith(('.jpg', '.jpeg', '.png')):
                # Clean up the URL by removing query parameters
                src = src.split('?')[0]
                images.add(src)

    # Remove pattern like "x100" from image URLs
    pattern = re.compile(r'x\d+')
    return [pattern.sub('', img) for img in images]

def scrape_vdp(vdp_url):
    """
    Scrape a single VDP page for VIN and image URLs.
    """
    try:
        html = fetch_html(vdp_url)
        soup = parse_html(html)
        vin = extract_vin(soup)
        images = extract_images(soup)
        return vin, images
    except Exception as e:
        print(f"Error scraping VDP URL {vdp_url}: {e}")
        return None, []
    
def main(url, start_index=0, end_index=0):
    """
    Main function to fetch and process VDP URLs from the sitemap.
    """
    parsed_url = urlparse(url)
    website_name = parsed_url.netloc
    sitemap_url = f'https://{website_name}/sitemap-inventory-sincro.xml'

    # Step 1: Get VDP URLs from Sitemap
    vdp_urls = get_vdp_urls_from_sitemap(sitemap_url)
    if end_index == 0 or end_index > len(vdp_urls):
        end_index = len(vdp_urls)
    
    # Step 2: Select a subset of VDP URLs based on provided indices
    vdp_urls = vdp_urls[start_index:end_index]

    # Step 3: Initialize data dictionary
    data = {'website_name': website_name, 'vins': {}}

    # Step 4: Process each VDP URL in parallel using ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=NUMBER_OF_WORKERS) as executor:
        results = list(executor.map(scrape_vdp, vdp_urls))

    # Step 5: Collect results into the data dictionary
    for vin, images in results:
        if vin:
            data['vins'][vin] = {'scraped_images_url': images}

    return data

# Example usage
url = "https://exampledealership.com"  # Replace with actual dealership URL
data = main(url, start_index=0, end_index=10)
print(data)