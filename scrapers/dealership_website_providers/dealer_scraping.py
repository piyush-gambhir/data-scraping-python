from concurrent.futures import ThreadPoolExecutor, as_completed
import os
from urllib.parse import urlparse
import re
import json
from selenium.webdriver.common.by import By

from web_scraping import setup_driver, fetch_html_content_using_selenium, fetch_html_content_using_requests, fetch_sitemap_using_requests, fetch_sitemap_using_selenium, parse_sitemap, create_directory, is_valid_image_url

NUMBER_OF_WORKERS = 5

vin_pattern = re.compile(r'[A-HJ-NPR-Z0-9]{17}')


def filter_urls(urls, pattern):
    return [url for url in urls if pattern in url]


def scrape_ansira(url):
    def extract_vin_data(soup):
        vin = None
        images = set()
        vin = None
        for text in soup.stripped_strings:
            match = vin_pattern.search(text)
            if match:
                vin = match.group()
                break
        for section in soup.find_all('section', id=re.compile(r'vdp-photos-dealershipPhotoGallery.*')):
            for img in section.find_all('img'):
                src = img.get('src')
                if src:
                    if (is_valid_image_url(src) == False):
                        continue
                    src = src.split('?')[0]
                    images.add(src)

        pattern = re.compile(r'x\d+')
        images = [pattern.sub('', img) for img in images]
        return vin, list(images)

    def process_url(url, website_name, data):
        soup = fetch_html_content_using_selenium(url, 0)

        vin, images = extract_vin_data(soup)

        if vin:
            data['vins'][vin] = {'scraped_images_url': images}

        with open(os.path.join(website_name, 'inventory_car_data.json'), 'w') as f:
            json.dump(data, f, indent=4)

    parsed_url = urlparse(url)
    website_name = parsed_url.netloc
    create_directory(website_name)
    sitemap_url = f'https://{website_name}/sitemap-inventory-sincro.xml'
    try:
        sitemap_content = fetch_sitemap_using_selenium(sitemap_url, 10)
        all_urls = parse_sitemap(sitemap_content)

        inventory_urls = []
        for url in all_urls:
            url_path_components = urlparse(url).path.split('/')
            if (url_path_components[-1] != ''):
                if (len(url_path_components) > 2):
                    inventory_urls.append(url)
                elif (len(url_path_components) >= 2 and url_path_components[1].count('-') >= parsed_url.path.split("/")[1].count("-") and any(char.isdigit() for char in url_path_components[1])):
                    inventory_urls.append(url)

        with open(os.path.join(website_name, 'inventory_car_urls.txt'), 'w') as f:
            f.writelines(", \n".join(inventory_urls))

        data = {
            "website_name": website_name,
            'vins': {}
        }

        with ThreadPoolExecutor(max_workers=NUMBER_OF_WORKERS) as executor:
            for url in inventory_urls:
                executor.submit(process_url, url, website_name, data)

    except Exception as e:
        print("An error occurred:", str(e))


def scrape_dealerdotcom(url):

    def extract_vin_data(soup):

        vin = soup.find('input', {'name': 'vin'})['value'] if soup.find(
            'input', {'name': 'vin'}) else 'No VIN found'
        images = [img['src'] for img in soup.select(
            '#media1-app-root img[src]') if is_valid_image_url(img['src'])]
        return vin, ', '.join(images)

    def process_url(url, website_name, data):
        soup = fetch_html_content_using_requests(url)
        vin, images = extract_vin_data(soup)

        if vin:
            data['vins'][vin] = {'scraped_images_url': images}

        with open(os.path.join(website_name, 'dealer_inventory_data.json'), 'w') as f:
            json.dump(data, f, indent=4)

    parsed_url = urlparse(url)
    website_name = parsed_url.netloc
    base_directory = create_directory(website_name)
    sitemap_url = f'https://{website_name}/sitemap.xml'
    try:
        sitemap_content = fetch_sitemap_using_requests(sitemap_url, 10)
        all_urls = parse_sitemap(sitemap_content)
        used_car_urls = filter_urls(all_urls, 'used/')
        new_car_urls = filter_urls(all_urls, 'new/')

        with open(os.path.join(website_name, 'dealer_inventory_urls.txt'), 'w') as f:
            f.writelines("\n".join(used_car_urls))
            f.writelines("\n".join(new_car_urls))

        data = {
            'website_url': website_name,
            'vins': {}
        }

        with ThreadPoolExecutor(max_workers=NUMBER_OF_WORKERS) as executor:
            futures = []
            for used_car_url in used_car_urls:
                futures.append(executor.submit(
                    process_url, used_car_url, website_name, data))
            for future in as_completed(futures):
                result = future.result()

    except Exception as e:
        print("An error occurred:", str(e))


def scrape_overfuel(url):

    def extract_vin_data(soup):
        vin = None
        for script in soup.find_all('script'):
            if script.string:
                match = vin_pattern.search(script.string)
                if match:
                    vin = match.group()
                    break
        image_elements = soup.select('img[src]')
        images = [img['src']
                  for img in image_elements if 'photos' in img['src']]

        return vin, ', '.join(images)

    def process_url(url, website_name, data):
        soup = fetch_html_content_using_requests(url)
        vin, images = extract_vin_data(soup)

        if vin:
            data['vins'][vin] = {'scraped_images_url': images}

        with open(os.path.join(website_name, 'inventory_car_data.json'), 'w') as f:
            json.dump(data, f, indent=4)

    website_name = parsed_url.netloc
    parsed_url = urlparse(url)
    sitemap_url = f'https://{website_name}/sitemap.xml'
    create_directory(website_name)
    try:
        sitemap_content = fetch_sitemap_using_requests(sitemap_url)
        all_urls = parse_sitemap(sitemap_content)
        used_car_urls = filter_urls(all_urls, 'inventory/')

        with open(os.path.join(website_name, 'inventory_car_urls.txt'), 'w') as f:
            f.writelines("\n".join(used_car_urls))

        data = {
            'website_url': website_name,
            'vins': {}
        }

        with ThreadPoolExecutor(max_workers=NUMBER_OF_WORKERS) as executor:
            futures = []
            for used_car_url in used_car_urls:
                futures.append(executor.submit(
                    process_url, used_car_url, website_name, data))
            for future in as_completed(futures):
                result = future.result()

    except Exception as e:
        print("An error occurred:", str(e))


def scrape_dealer_inspire(url):
    def extract_vin_data(soup, base_url):
        vin = None
        images = set()

        for script in soup.find_all('script'):
            if script.string:
                match = vin_pattern.search(script.string)
                if match:
                    vin = match.group()
                    break
        gallery_div = soup.find('div', id='gallery-modal')
        if gallery_div:
            for img in gallery_div.find_all('img'):
                src_urls = [img.get(attr)
                            for attr in ['src', 'data-src'] if img.get(attr)]
                for src_url in src_urls:
                    if src_url.startswith('/'):
                        src_url = base_url + src_url
                    if is_valid_image_url(src_url):
                        images.add(src_url)
        return vin, list(images)

    def process_url(url, parsed_url, website_name, data):
        soup = fetch_html_content_using_selenium(url, 30)
        vin, images = extract_vin_data(
            soup, base_url=f"{parsed_url.scheme}://{parsed_url.netloc}"
        )

        if vin:
            data['vins'][vin] = {'scraped_images_url': images}

        with open(os.path.join(website_name, 'inventory_car_data.json'), 'w') as f:
            json.dump(data, f, indent=4)

    parsed_url = urlparse(url)
    website_name = parsed_url.netloc
    sitemap_url = f'https://{website_name}/dealer-inspire-inventory/inventory_sitemap'

    create_directory(website_name)
    try:
        sitemap_content = fetch_sitemap_using_selenium(sitemap_url, 15)
        urls = parse_sitemap(sitemap_content)
        inventory_urls = filter_urls(urls, '/inventory')
        with open(os.path.join(website_name, 'inventory_car_urls.txt'), 'w') as f:
            f.writelines(", \n".join(inventory_urls))

        data = {
            'website_url': website_name,
            'vins': {}
        }

        with ThreadPoolExecutor(max_workers=1) as executor:
            futures = []
            for inventory_url in inventory_urls:
                futures.append(executor.submit(
                    process_url, inventory_url, parsed_url, website_name, data))
            for future in as_completed(futures):
                result = future.result()

    except Exception as e:
        print("An error occurred:", str(e))


def scrape_dealer_car_search(url):

    def extract_vin_data(soup):
        vin = None
        images = set()
        vin = None
        for text in soup.stripped_strings:
            match = vin_pattern.search(text)
            if match:
                vin = match.group()
                break

        for img in soup.find_all('img'):
            src = img.get('data-src')
            if src and is_valid_image_url(src):
                images.add(src)
        return vin, list(images)

    def process_url(url, website_name, data):
        soup = fetch_html_content_using_requests(url)
        vin, images = extract_vin_data(soup)

        if vin:
            data['vins'][vin] = {'scraped_images_url': images}

        with open(os.path.join(website_name, 'inventory_car_data.json'), 'w') as f:
            json.dump(data, f, indent=4)

    parsed_url = urlparse(url)
    website_name = parsed_url.netloc
    create_directory(website_name)
    sitemap_url = f'https://{website_name}/sitemap.xml'
    try:
        sitemap_content = fetch_sitemap_using_requests(sitemap_url)
        all_urls = parse_sitemap(sitemap_content)

        inventory_urls = []
        for url in all_urls:
            url_path_components = urlparse(url).path.split('/')
            if (url_path_components[-1] != ''):
                if (len(url_path_components) > 2):
                    inventory_urls.append(url)
                elif (len(url_path_components) >= 2 and url_path_components[1].count('-') >= parsed_url.path.split("/")[1].count("-") and any(char.isdigit() for char in url_path_components[1])):
                    inventory_urls.append(url)

        with open(os.path.join(website_name, 'inventory_car_urls.txt'), 'w') as f:
            f.writelines(", \n".join(inventory_urls))

        data = {
            "website_name": website_name,
            'vins': {}
        }

        for (url) in inventory_urls:
            process_url(url, website_name, data)

    except Exception as e:
        print("An error occurred:", str(e))


def scrape_random(url, custom_sitemap_url=None, vin_x_path=None, images_container_x_path=None):
    def get_highest_resolution_image(srcset):

        highest_res = 0
        highest_res_url = None
        for entry in srcset.split(","):
            parts = entry.strip().split(" ")
            if len(parts) == 2 and parts[1].endswith("w"):
                res = int(parts[1][:-1])
                if res > highest_res:
                    highest_res = res
                    highest_res_url = parts[0]
        return highest_res_url

    def extract_vin_data(soup, base_url, driver, vin_x_path, image_container_x_path):
        vin = None
        images = set()
        if vin_x_path:
            vin = driver.find_element(by=By.XPATH, value=vin_x_path).text
        else:
            vin_pattern = re.compile(r'[A-HJ-NPR-Z0-9]{17}')
            vin = None
            for text in soup.stripped_strings:
                match = vin_pattern.search(text)
                if match:
                    vin = match.group()
                    break

        if image_container_x_path:
            image_elements = driver.find_element(
                by=By.XPATH, value=image_container_x_path).find_elements(By.TAG_NAME, 'img')
            for img in image_elements:
                if img.get_attribute('src'):
                    img_url = img.get_attribute('src')
                    img_url = img_url.split('?')[0]
                    if img_url.startswith('/'):
                        img_url = base_url + img_url
                    if is_valid_image_url(img_url):
                        images.add(img_url)
        else:
            for img in soup.find_all('img'):
                src_url = img.get('src') or img.get('data-src')
                src_url = src_url.split('?')[0]
                if src_url:
                    if src_url.startswith('/'):
                        src_url = base_url + src_url
                    if is_valid_image_url(src_url):
                        images.add(src_url)

                srcset = img.get('srcset')
                if srcset:
                    highest_res_image = get_highest_resolution_image(srcset)
                    if highest_res_image:
                        if highest_res_image.startswith('/'):
                            highest_res_image = base_url + highest_res_image
                        if is_valid_image_url(highest_res_image):
                            images.add(highest_res_image)
        print(f"VIN: {vin}")
        print(f"Images: {images}")
        return vin, list(images)

    def process_url(url, parsed_url, website_name, data, vin_x_path, image_container_x_path):
        driver = setup_driver()
        soup = fetch_html_content_using_selenium(url)
        vin, images = extract_vin_data(
            soup,
            base_url=f"{parsed_url.scheme}://{parsed_url.netloc}",
            driver=driver,
            vin_x_path=vin_x_path,
            image_container_x_path=image_container_x_path
        )

        if vin:
            data['vins'][vin] = {'scraped_images_url': images}

        with open(os.path.join(website_name, 'inventory_car_data.json'), 'w') as f:
            json.dump(data, f, indent=4)

        driver.quit()

    parsed_url = urlparse(url)
    website_name = parsed_url.netloc
    create_directory(website_name)

    sitemap_url = custom_sitemap_url or f'https://{website_name}/sitemap.xml'
    try:
        sitemap_content = fetch_sitemap_using_selenium(sitemap_url, 15)
        all_urls = parse_sitemap(sitemap_content)

        inventory_urls = []
        for url in all_urls:
            url_path_components = urlparse(url).path.split('/')
            if (url_path_components[-1] != ''):
                if (len(url_path_components) > 2):
                    inventory_urls.append(url)
                elif (len(url_path_components) >= 2 and url_path_components[1].count('-') >= parsed_url.path.split("/")[1].count("-") and any(char.isdigit() for char in url_path_components[1])):
                    inventory_urls.append(url)

        with open(os.path.join(website_name, 'inventory_car_urls.txt'), 'w') as f:
            f.writelines(", \n".join(inventory_urls))

        data = {
            website_name: website_name,
            'vins': {}
        }

        with ThreadPoolExecutor(max_workers=NUMBER_OF_WORKERS) as executor:
            future_to_url = {executor.submit(process_url, url, parsed_url, website_name,
                                             data, vin_x_path, images_container_x_path): url for url in inventory_urls}

            for future in as_completed(future_to_url):
                url = future_to_url[future]
                try:
                    future.result()

                except Exception as exc:
                    print(f"{url} generated an exception: {exc}")

    except Exception as e:
        print("An error occurred:", str(e))
