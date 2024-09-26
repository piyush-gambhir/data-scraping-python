# Importing the libraries
import os
import requests
import urllib
from bs4 import BeautifulSoup
import csv
import pandas as pd
import json

# List of all the URLs to scrape
# Read the urls from a txt file
with open('urls.txt', 'r') as txt_file:
    urls = txt_file.read().split(', \n')
    urls = [url.strip() for url in urls]

# Create a folder to store all the outputs
output_folder = 'output'
os.makedirs(output_folder, exist_ok=True)

# Dictionary to store the CARFAX report URLs
carfax_report_dict = {}

# List of all the URL's that failed to scrape
failed_urls = []

# Create a JSON file to store all the data of all the URLs
output_filename_json = "cars_data.json"
output_filepath_json = os.path.join(output_folder, output_filename_json)

# Create a CSV file to store all the data of all the URLs
output_filename_csv = "cars_data.csv"
output_filepath_csv = os.path.join(output_folder, output_filename_csv)

# Creating a data list to store all the data
data_list = []


# Loop through all the URLs
for url in urls:
    try:
        # Parse the HTML content using BeautifulSoup
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        """
        Extracting Vehicle Details
        """
        # Getting the listing title
        listing_title = soup.find(
            'h1', {'class': 'listing-title'}).text.strip()
        # Getting the listing price
        listing_price = soup.find(
            'span', {'class': 'primary-price'}).text.strip()

        """
        Extracting the Vehicle Features
        """
        features_dict = {
            'Features': [],
        }
        modal = soup.find('div', {'class': 'all-features-text-container'})
        for bullet_point in modal.find_all('li'):
            feature = bullet_point.text.strip()
            features_dict['Features'].append(feature)

        """
        Extracting Description Lists
        """
        description_lists_dict = {
            'Attribute': [],
            'Description': []
        }

        description_lists = soup.find_all('dl')
        for dl in description_lists:
            dt_elements = dl.find_all('dt')
            dd_elements = dl.find_all('dd')
            for dt, dd in zip(dt_elements, dd_elements):
                term = dt.text.strip()
                description = dd.text.strip()
                description_lists_dict['Attribute'].append(term)
                description_lists_dict['Description'].append(description)

        # Creating a dictionary for the data
        data_dict = {
            'Listing Title': listing_title,
            'Listing Price': listing_price,
            'Features': ", ".join(features_dict['Features']),
        }

        for attribute, description in zip(description_lists_dict['Attribute'], description_lists_dict['Description']):
            data_dict[attribute] = description

        # Unique Listing Title
        unique_listing_title = f"{description_lists_dict['Description'][7]}_{listing_title.replace('/', '_').replace(' ', '_')}"

        # # Create a folder to store all the outputs (i.e. images, details csv file)
        # folder_name = unique_listing_title
        # folder_path = os.path.join(output_folder, folder_name)
        # os.makedirs(folder_path, exist_ok=True)

        # """
        # Extracting the Vehicle Images
        # """
        # div_carousel = soup.find(
        #     'gallery-slides', {'aria-label': 'Image carousel'})
        # images = div_carousel.find_all('img')
        # image_folder = os.path.join(folder_path, 'images')
        # os.makedirs(image_folder, exist_ok=True)
        # for i, image in enumerate(images, start=1):
        #     image_url = image['src']
        #     filename = os.path.join(
        #         image_folder, f'{unique_listing_title}_image_{i}.jpg')
        #     urllib.request.urlretrieve(image_url, filename)

        """
        Extracting the Vehicle Images
        """
        image_folder = os.path.join(output_folder, 'images')
        os.makedirs(image_folder, exist_ok=True)
        div_carousel = soup.find(
            'gallery-slides', {'aria-label': 'Image carousel'})
        images = div_carousel.find_all('img')
        for i, image in enumerate(images, start=1):
            image_url = image['src']
            filename = os.path.join(
                image_folder, f'{unique_listing_title}_image_{i}.jpg')
            if (os.path.exists(filename)):
                continue
            else:
                urllib.request.urlretrieve(image_url, filename)

        """
        Extracting the CARFAX Report Links
        """
        carfax_report = soup.find(
            'a', {'data-nav-click-intent-id': 'vdp-vehicle-history-report'})
        carfax_report_url = carfax_report['href']
        carfax_report_url = 'https://www.cars.com' + carfax_report_url

        # Get the final URL
        response = requests.get(carfax_report_url)
        carfax_report_url = response.url

        # # Save the final listing_title and final_url to a dictionary
        # carfax_report_dict[unique_listing_title] = carfax_report_url

        data_dict['CARFAX Report URL'] = carfax_report_url

        data_list.append(data_dict)
    except Exception as e:
        print(e)
        print(f'Error for {url}')
        failed_urls.append(url)

# write the failed urls to a txt file seperated by comma
output_filename = "failed_urls.txt"
output_filepath = os.path.join(output_folder, output_filename)
with open(output_filepath, 'w') as txt_file:
    for url in failed_urls:
        txt_file.write("'" + url + "'" + ", ")

# # write the dictionary to a csv file
# output_filename = "carfax_report_links.csv"
# output_filepath = os.path.join(output_folder, output_filename)
# field_names = ['Name', 'URL']
# with open(output_filepath, 'w', newline='') as csv_file:
#     writer = csv.DictWriter(csv_file, fieldnames=field_names)
#     writer.writeheader()
#     for name, url in carfax_report_dict.items():
#         writer.writerow({'Name': name, 'URL': url})


# write the dictionary to a json file (if exisits continue, else create a new file)
if os.path.exists(output_filepath_json):
    with open(output_filepath_json, 'r') as json_file:
        data = json.load(json_file)
        data.update(data_list)
    with open(output_filepath_json, 'w') as json_file:
        json.dump(data, json_file, indent=4)
else:
    with open(output_filepath_json, 'w') as json_file:
        json.dump(data_list, json_file, indent=4)

# write the dictionary to a csv file (if exisits continue, else create a new file)
if os.path.exists(output_filepath_csv):
    df = pd.read_csv(output_filepath_csv)
    df = df.append(data_list, ignore_index=True)
    df.to_csv(output_filepath_csv, index=False)
else:
    df = pd.DataFrame(data_list)
    df.to_csv(output_filepath_csv, index=False)
