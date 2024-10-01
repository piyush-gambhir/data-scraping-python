import os
import requests

def create_folder(folder_name):
    try:
        os.mkdir(folder_name)
    except FileExistsError:
        pass  # No need to print every time when the folder already exists.

def extract_folder_name_from_url(url):
    """Extracts the folder name from the given URL."""
    # Split the URL at '%2Fcars%2F' and take the next section until '&'
    return url.split('%2Fcars%2F')[1].split('&')[0]

def save_car_data(base_folder, make, model, stock_number, image_url_template):
    make_folder_path = os.path.join(base_folder, make)
    create_folder(make_folder_path)

    model_folder_path = os.path.join(make_folder_path, str(model))
    create_folder(model_folder_path)

    stock_number_folder_path = os.path.join(model_folder_path, str(stock_number))
    create_folder(stock_number_folder_path)

    for x in range(1, 61):
        image_url = image_url_template.replace('{stock_number}', str(stock_number)).replace('{x}', str(x))
        image_response = requests.get(image_url)
        image_filename = f"{stock_number}_{x}.jpg"
        image_file_path = os.path.join(stock_number_folder_path, image_filename)
        with open(image_file_path, 'wb') as image_file:
            image_file.write(image_response.content)
            
def scrape_cars_details(url, take=24):
    folder_name = extract_folder_name_from_url(url)
    base_folder = os.path.join(os.getcwd(), folder_name)
    create_folder(base_folder)

    # Rest of your function...
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
        'Accept': 'application/json',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive',
    }

    skip = 0
    processed_stock_numbers = set()
    count = 0
    while True:
        current_url = f"{url}&skip={skip}&take={take}"
        if skip != 0:
            current_url += "&scoringProfile=GenericV2"

        response = requests.get(current_url, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch the API response. Status Code: {response.status_code}")
            break

        data = response.json()
        car_list = data.get('items', [])

        if not car_list:
            # No more data, break the loop
            break

        for car_data in car_list:
            make = car_data.get('make')
            model = car_data.get('model')
            stock_number = car_data.get('stockNumber')
            count += 1

            if make and model and stock_number:
                if stock_number in processed_stock_numbers:
                    # Skip processing this car as it's already processed
                    continue

                # Save the car data in a subfolder based on 'model', inside the 'make' folder
                save_car_data(base_folder, make, model, stock_number, 
                              image_url_template='https://img2.carmax.com/assets/{stock_number}/360-exterior/{x}.jpg?width=1600&height=900')

                # Add the stock number to the processed set
                processed_stock_numbers.add(stock_number)
            else:
                print("Could not find car details for this element.")
        
        # Increment the skip value for the next page
        skip += take

if __name__ == "__main__":
    urls = [
        'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%2Fcoupes&zipCode=66204&radius=radius-nationwide&shipping=-1&sort=best-match&visitorID=deb7cb97-eecd-461c-a072-cec8f8b0db06',
               'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%2Fconvertibles&zipCode=66204&radius=radius-nationwide&shipping=-1&sort=best-match&visitorID=deb7cb97-eecd-461c-a072-cec8f8b0db06',
        'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%2Fcrossovers&zipCode=66204&radius=radius-nationwide&shipping=-1&sort=best-match&visitorID=deb7cb97-eecd-461c-a072-cec8f8b0db06',
        'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%2Fhatchbacks&zipCode=66204&radius=radius-nationwide&shipping=-1&sort=best-match&visitorID=deb7cb97-eecd-461c-a072-cec8f8b0db06',
        'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%2Fluxury-vehicles&zipCode=66204&radius=radius-nationwide&shipping=-1&sort=best-match&visitorID=deb7cb97-eecd-461c-a072-cec8f8b0db06',
        'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%2Fminivans-and-vans&zipCode=66204&radius=radius-nationwide&shipping=-1&sort=best-match&visitorID=deb7cb97-eecd-461c-a072-cec8f8b0db06',
        'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%2Fpickup-trucks&zipCode=66204&radius=radius-nationwide&shipping=-1&sort=best-match&visitorID=deb7cb97-eecd-461c-a072-cec8f8b0db06',
        'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%2Fsedans&zipCode=66204&radius=radius-nationwide&shipping=-1&sort=best-match&visitorID=deb7cb97-eecd-461c-a072-cec8f8b0db06',
        'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%2Fsports-cars&zipCode=66204&radius=radius-nationwide&shipping=-1&sort=best-match&visitorID=deb7cb97-eecd-461c-a072-cec8f8b0db06',
        'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%2Fsport-utilities&zipCode=66204&radius=radius-nationwide&shipping=-1&sort=best-match&visitorID=deb7cb97-eecd-461c-a072-cec8f8b0db06',
        'https://www.carmax.com/cars/api/search/run?uri=%2Fcars%2Fwagons&zipCode=66204&radius=radius-nationwide&shipping=-1&sort=best-match&visitorID=deb7cb97-eecd-461c-a072-cec8f8b0db06']
    for url in urls:
        scrape_cars_details(url)
