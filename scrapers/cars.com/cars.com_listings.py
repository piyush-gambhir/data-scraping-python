from selenium.webdriver.common.by import By
import time

from helpers.selenium.webdriver import create_firefox_driver
from helpers.url.url import construct_url
from helpers.json.append import append_json
from helpers.csv.append import append_csv


def fetch_vehicle_cards(driver, url):
    """
    Navigates to the URL and fetches vehicle cards.
    """
    driver.get(url)
    time.sleep(5)  # Wait for the page to load fully
    return driver.find_elements(By.CLASS_NAME, 'vehicle-card-main')


def extract_vehicle_data(vehicle_card):
    """
    Extracts data from a single vehicle card.
    """
    try:
        car_name = vehicle_card.find_element(By.CLASS_NAME, 'title').text or ""
    except Exception:
        car_name = ""

    try:
        car_price = vehicle_card.find_element(
            By.CLASS_NAME, 'primary-price').text or ""
    except Exception:
        car_price = ""

    try:
        dealer_name = vehicle_card.find_element(
            By.CLASS_NAME, 'dealer-name').text or ""
    except Exception:
        dealer_name = ""

    try:
        dealer_location = vehicle_card.find_element(
            By.CLASS_NAME, 'miles-from').text or ""
    except Exception:
        dealer_location = ""

    try:
        mileage = vehicle_card.find_element(
            By.CLASS_NAME, 'mileage').text or ""
    except Exception:
        mileage = ""

    try:
        image_elements = vehicle_card.find_elements(
            By.CSS_SELECTOR, '.vehicle-card-photos img')
        image_urls = [img.get_attribute('src') for img in image_elements] or []
    except Exception:
        image_urls = []

    try:
        condition = vehicle_card.find_element(
            By.CLASS_NAME, 'stock-type').text or ""
    except Exception:
        condition = ""

    try:
        # Extract VIN using data-vin attribute from the spark-button element
        vin = vehicle_card.find_element(
            By.CSS_SELECTOR, 'spark-button[data-vin]').get_attribute('data-vin') or ""
    except Exception:
        vin = ""

    try:
        vdp_url = vehicle_card.find_element(
            By.CLASS_NAME, 'vehicle-card-link').get_attribute('href') or ""
    except Exception:
        vdp_url = ""

    return {
        "name": car_name,
        "price": car_price,
        "dealer": dealer_name,
        "location": dealer_location,
        "mileage": mileage,
        "image_urls": image_urls,
        "condition": condition,
        "vin": vin,
        "vdp_url": vdp_url
    }


def main():
    zipcode = ""
    make = ""
    model = ""
    year_max = ""
    year_min = ""
    maximum_distance = ""
    page_size = "100"
    page = 1

    # Initialize WebDriver
    driver = create_firefox_driver()

    try:

        while True:
            # Construct the URL
            url = construct_url(
                scheme="https",
                netloc="www.cars.com",
                path="/shopping/results/",
                query_params={
                    "stock_type": "all",
                    "makes[]": make,
                    "models[]": model,
                    "maximum_distance": maximum_distance,
                    "zipcode": zipcode,
                    "page_size": page_size,
                    "page": page,
                    "year_max": year_max,
                    "year_min": year_min
                }
            )

            # Fetch vehicle cards
            vehicle_cards = fetch_vehicle_cards(driver, url)

            # If no vehicle cards are found, break the loop
            if not vehicle_cards:
                print(f"No data found on page {page}. Stopping.")
                break

            # Initialize a list to store car data
            car_data = []

            # Loop through each vehicle card and extract data
            for vehicle_card in vehicle_cards:
                vehicle_info = extract_vehicle_data(vehicle_card)
                if vehicle_info:
                    car_data.append(vehicle_info)

            # Save data to JSON
            append_json("cars.com_listing_data.json", car_data)

            # Save data to CSV
            append_csv("cars.com_listing_data.csv", car_data, ['name', 'price', 'dealer', 'location',
                                                               'mileage', 'image_urls', 'condition', 'vin', 'vdp_url'])

            # Increment the page number
            print(f"Page {page} done.")
            page += 1

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the WebDriver
        driver.quit()


if __name__ == "__main__":
    main()
