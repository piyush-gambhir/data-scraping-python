from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv

# Set up Chrome WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)

# URL of the Google Maps search for car dealerships in Alabama
url = "https://www.google.com/maps/search/car+dealerships+in+Alabama+USA/"

# Open the web page
driver.get(url)

# Handle cookie consent if present
try:
    cookie_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(@class, 'VfPpkd-LgbsSe')]"))
    )
    cookie_button.click()
    print("Clicked consent to cookies.")
except Exception as e:
    print(f"No cookie consent found or required. Exception: {e}")

# Wait for the page to load (implicit wait)
driver.implicitly_wait(30)

# Function to scroll until no new data is loaded


def scroll_until_no_new_data(driver, panel_xpath, pause_time):
    panel_element = driver.find_element(By.XPATH, panel_xpath)
    actions = ActionChains(driver)
    actions.move_to_element(panel_element).click().perform()

    previous_count = 0
    consecutive_no_change = 0
    max_no_change = 6  # Increase number of scrolls to ensure more dealerships load

    while consecutive_no_change < max_no_change:
        actions.send_keys(Keys.PAGE_DOWN).perform()
        time.sleep(pause_time)

        # Check the number of loaded titles (dealership names)
        page_source = driver.page_source
        # Update class name if needed
        titles = driver.find_elements(By.CLASS_NAME, 'hfpxzc')

        current_count = len(titles)
        print(f"Loaded {current_count} dealerships so far...")

        if current_count == previous_count:
            consecutive_no_change += 1
        else:
            consecutive_no_change = 0  # Reset if new data was found

        previous_count = current_count
        print(f"Scrolling... New dealerships loaded: {current_count}")


# Scroll the results panel to load all dealership data
panel_xpath = "//*[@id='QA0Szd']/div/div/div[1]/div[2]/div"
# Increased scroll pause time
scroll_until_no_new_data(driver, panel_xpath, pause_time=3)

# Function to explicitly wait for an element to load


def wait_for_element_to_load(driver, xpath, timeout=15):
    try:
        element = WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        return element
    except Exception as e:
        print(f"Error waiting for element: {e}")
        return None

# Function to click using JavaScript to avoid click interception issues


def click_element_js(driver, element):
    try:
        driver.execute_script("arguments[0].click();", element)
    except Exception as e:
        print(f"Error clicking element: {e}")

# Parse dealership data from each listing


def extract_dealership_info(driver, index):
    try:
        # Find the dealership element and scroll into view
        dealership_element = driver.find_element(
            By.XPATH, f"(//*[@class='hfpxzc'])[{index + 1}]")

        # Scroll to the element to ensure it's visible
        driver.execute_script(
            "arguments[0].scrollIntoView();", dealership_element)
        time.sleep(1)

        # Click the dealership name using JavaScript to avoid the interception issue
        click_element_js(driver, dealership_element)
        time.sleep(2)  # Allow time for the details to load

        # Wait for address, phone, and other details to load
        address = wait_for_element_to_load(
            driver, "//span[contains(@class, 'LrzXr')]", timeout=5)
        phone = wait_for_element_to_load(
            driver, "//span[contains(@class, 'LrzXr kno-fv')]", timeout=5)

        # Extract text or fallback to 'N/A'
        address_text = address.text if address else 'N/A'
        phone_text = phone.text if phone else 'N/A'

        # Close the dealership details panel
        back_button = wait_for_element_to_load(
            driver, "//button[@aria-label='Back']", timeout=5)
        if back_button:
            click_element_js(driver, back_button)

        return address_text, phone_text

    except Exception as e:
        print(f"Error extracting dealership info at index {index}: {e}")
        return 'N/A', 'N/A'


# Get the page HTML source and parse it with BeautifulSoup
page_source = driver.page_source
# Ensure the class name is correct for titles
titles = driver.find_elements(By.CLASS_NAME, 'hfpxzc')

# CSV file path to save the data
csv_file_path = 'dealerships_alabama.csv'

# Write the dealership data to the CSV file
with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Dealership', 'Address', 'Phone Number'])

    for index, title in enumerate(titles):
        # Extract the title (dealership name)
        title_text = title.get_attribute('aria-label') if title else 'N/A'

        # Extract more details by interacting with the dealership card
        address, phone_number = extract_dealership_info(driver, index)

        # Write the row to the CSV file
        csv_writer.writerow([title_text, address, phone_number])

print(f"Data has been saved to '{csv_file_path}'")

# Prevent premature window closure
input("Press Enter to close the browser...")

# Close the WebDriver
driver.quit()
