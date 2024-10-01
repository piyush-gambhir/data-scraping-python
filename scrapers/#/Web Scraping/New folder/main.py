import pandas as pd
import os
import requests
import csv
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import re
import time
from selenium import webdriver
import concurrent.futures


def setup_driver():
    driver = webdriver.Firefox()
    return driver


def fetch_sitemap_using_requests(url):
    response = requests.get(url)
    return response.text


def fetch_sitemap_using_selenium(url, sleep_time=30):
    driver = setup_driver()
    driver.get(url)
    time.sleep(sleep_time)
    response = driver.page_source
    driver.quit()
    return response


def extract_namespace(xml_content):
    match = re.search(r'\s*<urlset\s+xmlns="([^"]+)"', xml_content)
    if match:
        namespace = match.group(1)
        print(f"Extracted namespace: {namespace}")  # Debug print
        return namespace
    else:
        print("No namespace found")  # Debug print
    return None


def parse_sitemap(sitemap_content):
    # Try to extract the namespace dynamically from the content
    namespace = extract_namespace(sitemap_content)
    if namespace:
        try:
            root = ET.fromstring(sitemap_content)
            # Extract URLs with the detected namespace
            urls = [elem.text for elem in root.findall(
                f'.//{{{namespace}}}loc')]
            if urls:  # If URLs are found, return them
                return urls
        except ET.ParseError:
            pass  # Continue to fallback HTML parsing

    try:
        # root = ET.fromstring(sitemap_content)
        # urls = [elem.text for elem in root.findall('.//loc')]
        # return urls
        root = ET.fromstring(sitemap_content)
        return [elem.text for elem in root.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    except ET.ParseError:
        pass
    # If XML parsing fails or no namespace detected, try parsing as HTML
    try:
        soup = BeautifulSoup(sitemap_content, 'html.parser')
        links = soup.find_all('a')
        urls = [link.get('href') for link in links]
        return urls
    except Exception as e:
        # Print error and return an empty list for any other exceptions
        print(f"An error occurred: {e}")
        return []


def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)


def filter_urls(urls, pattern):
    return [url for url in urls if pattern in url]


def save_urls_to_csv(urls, provider_name, website_name):
    # Create directory if it doesn't exist
    if not os.path.exists(provider_name):
        os.makedirs(provider_name)

    filename = os.path.join(provider_name, f"{website_name}.csv")
    with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for url in urls:
            writer.writerow([url])

# Provider-Specific Logic


def get_ansira_vdp_urls(dealer_website_url):
    if not dealer_website_url.startswith('http'):
        dealer_website_url = 'https://' + dealer_website_url

    parsed_url = urlparse(dealer_website_url)
    website_name = parsed_url.netloc
    sitemap_url = f'https://{website_name}/sitemap.xml'

    sitemap_content = fetch_sitemap_using_requests(sitemap_url)
    all_urls = parse_sitemap(sitemap_content)

    inventory_urls = []
    for url in all_urls:
        if any(segment in url for segment in ['/used', '/new', '/certified']):
            inventory_urls.append(url)
    return inventory_urls


def get_dealer_dot_com_vdp_urls(dealer_website_url):
    parsed_url = urlparse(dealer_website_url)
    website_name = parsed_url.netloc
    sitemap_url = f'https://{website_name}/sitemap.xml'

    sitemap_content = fetch_sitemap_using_requests(sitemap_url)
    if sitemap_content:
        all_urls = parse_sitemap(sitemap_content)
        used_car_urls = filter_urls(all_urls, 'used/')
        new_car_urls = filter_urls(all_urls, 'new/')
        return used_car_urls + new_car_urls
    return []


def get_overfuel_vdp_urls(dealer_website_url):
    parsed_url = urlparse(dealer_website_url)
    website_name = parsed_url.netloc
    sitemap_url = f'https://{website_name}/sitemap.xml'

    sitemap_content = fetch_sitemap_using_requests(sitemap_url)
    if sitemap_content:
        all_urls = parse_sitemap(sitemap_content)
        return filter_urls(all_urls, 'inventory/')
    return []


def get_dealer_inspire_vdp_urls(dealer_website_url):
    if not dealer_website_url.startswith('http'):
        dealer_website_url = 'https://' + dealer_website_url

    parsed_url = urlparse(dealer_website_url)
    website_name = parsed_url.netloc
    sitemap_url = f'https://{website_name}/dealer-inspire-inventory/inventory_sitemap'

    sitemap_content = fetch_sitemap_using_requests(sitemap_url)
    if sitemap_content:
        all_urls = parse_sitemap(sitemap_content)
        return filter_urls(all_urls, '/inventory')
    return []


def get_autocorner_vdp_urls(dealer_website_url):
    parsed_url = urlparse(dealer_website_url)
    website_name = parsed_url.netloc
    sitemap_url = f'https://{website_name}/sitemap.xml'

    sitemap_content = fetch_sitemap_using_requests(sitemap_url)
    if sitemap_content:
        all_urls = parse_sitemap(sitemap_content)
        return filter_urls(all_urls, 'vehicles/')
    return []

# Main Function to process all websites


def process_single_website(row):
    scraped_status = []
    dealer_website = row['Dealer_Website']
    website_provider = row['Website Provider']
    print(f"Processing {dealer_website} ({website_provider})")

    try:
        if 'Ansira' in website_provider:
            vdp_urls = get_ansira_vdp_urls(dealer_website)
        elif 'Dealer.com' in website_provider:
            vdp_urls = get_dealer_dot_com_vdp_urls(dealer_website)
        elif 'Auto Corner' in website_provider:
            vdp_urls = get_autocorner_vdp_urls(dealer_website)
        elif 'Dealer Inspire' in website_provider:
            vdp_urls = get_dealer_inspire_vdp_urls(dealer_website)
        else:
            print(f"Provider {website_provider} is not supported yet.")
            return (dealer_website, website_provider, False)

        if vdp_urls:
            save_urls_to_csv(vdp_urls, website_provider, dealer_website)
            print(f"Saved {len(vdp_urls)} VDP URLs for {dealer_website}")
            return (dealer_website, website_provider, True)
        else:
            print(f"No VDP URLs found for {dealer_website}")
            return (dealer_website, website_provider, False)

    except Exception as e:
        print(f"An error occurred while processing {dealer_website}: {e}")
        return (dealer_website, website_provider, False)


def process_website_vdp_urls_concurrently(website_df, num_workers=10):
    scraped_status = []

    # Use ThreadPoolExecutor to run the process in parallel
    with concurrent.futures.ThreadPoolExecutor(max_workers=num_workers) as executor:
        # Submit each row in the DataFrame as a task
        futures = [executor.submit(process_single_website, row)
                   for _, row in website_df.iterrows()]

        # As each task completes, append its result to the status list
        for future in concurrent.futures.as_completed(futures):
            result = future.result()
            if result:
                scraped_status.append(result)

            # Save the scraped status to a CSV file after each iteration
            status_df = pd.DataFrame(scraped_status, columns=[
                                     'Dealer_Website', 'Website_Provider', 'Scraped'])
            status_df.to_csv('scraped_status.csv', index=False)


# Sample website data (replace with actual dataframe)
website_df = pd.read_csv('combined_dealer_websites.csv')

# Run the process with 10 concurrent workers
process_website_vdp_urls_concurrently(website_df, num_workers=10)
