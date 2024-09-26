

from bs4 import BeautifulSoup
import requests


def get_car_urls_with_carfax(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Parse the HTML content of the page with BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Find all car URLs that have a Carfax report
    car_urls_with_carfax = []
    count = 0
    url_prefix = 'https://www.cars.com'
    for car_div in soup.find_all('div', class_='vehicle-card'):
        external_link_div = soup.find(
            'div', class_='vehicle-links external-links')
        print(external_link_div)
        if 'CARFAX' in external_link_div.find('a', class_='sds-link--ext').text:
            print(car_div.find('a')['href']
            car_url = url_prefix + car_div.find('a')['href']
            car_urls_with_carfax.append(car_url)
            count += 1
    print(count)
    return car_urls_with_carfax


# Use the function
url = 'https://www.cars.com/shopping/results/?city_name=Victoria%2C+TX&city_slug[]=victoria-tx&page=1&page_size=100&stock_type=used&zip=77901'
car_urls_with_carfax = get_car_urls_with_carfax(url)

# Write to TXT file separated by commas
with open('car_urls_with_carfax.txt', 'w') as f:
    for car_url in car_urls_with_carfax:
        f.write(car_url + ", \n")
