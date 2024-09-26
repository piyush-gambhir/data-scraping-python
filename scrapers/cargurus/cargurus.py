import time
import csv
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

'''
mechanisms that prevent automated scraping
'''

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument("--headless")  # Comment this out to run with GUI
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")

# Initialize the WebDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=chrome_options)
actions = ActionChains(driver)

# Define login credentials
email = "demoldo@gmail.com"
password = "JMXP#Re%A?5L7m6"

# Step 1: Open the login page
login_url = "https://www.cargurus.com/Cars/authentication/renderRegisterLoginForm.action?redirectUrl=%2F"
driver.get(login_url)
time.sleep(2)  # Add a delay to mimic human interaction

# Step 2: Enter email
try:
    email_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="registerEmail"]'))
    )
    actions.move_to_element(email_input).perform()
    email_input.send_keys(email)
    time.sleep(1)  # Add a delay to mimic human interaction
except Exception as e:
    print(f"Error finding email input: {e}")
    driver.quit()
    exit(1)

# Step 3: Click Next button
try:
    next_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="outsideModal"]/div/div/div[2]/div/form/button'))
    )
    actions.move_to_element(next_button).perform()
    next_button.click()
    time.sleep(2)  # Add a delay to mimic human interaction
except Exception as e:
    print(f"Error clicking Next button: {e}")
    driver.quit()
    exit(1)

# Wait for the user to manually solve the CAPTCHA if it appears
input("Please solve the CAPTCHA manually and then press Enter here...")

# Step 4: Enter password
try:
    password_input = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="loginPassword"]'))
    )
    actions.move_to_element(password_input).perform()
    password_input.send_keys(password)
    time.sleep(1)  # Add a delay to mimic human interaction
except Exception as e:
    print(f"Error finding password input: {e}")
    driver.quit()
    exit(1)

# Step 5: Submit the login form
try:
    submit_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="outsideModal"]/div/div/div[2]/div/form/button'))
    )
    actions.move_to_element(submit_button).perform()
    submit_button.click()
    time.sleep(2)  # Add a delay to mimic human interaction
except Exception as e:
    print(f"Error submitting login form: {e}")
    driver.quit()
    exit(1)

# Step 6: Wait for the login to complete and navigate to the target page
inventory_url = "https://www.cargurus.com/Cars/inventorylisting/viewDetailsFilterViewInventoryListing.action?sourceContext=carGurusHomePageModel&entitySelectingHelper.selectedEntity=m43&zip=95124"
driver.get(inventory_url)
time.sleep(2)  # Add a delay to mimic human interaction

# Wait for the page to load and for the specific element to be present
try:
    WebDriverWait(driver, 20).until(
        EC.presence_of_element_located(
            (By.XPATH, '//*[@id="cargurus-listing-search"]/div/div/div[2]/div[2]/div[3]/div/div/div/a/div[2]/div/div[2]'))
    )
    print("Landed!!")
except Exception as e:
    print(f"Error waiting for page to load: {e}")
    driver.quit()
    exit(1)

# Locate all car titles
titles = driver.find_elements(
    By.XPATH, '//*[@id="cargurus-listing-search"]/div/div/div[2]/div[2]/div[3]/div/div/div/a/div[2]/div/div[2]')

# Extract text from elements
car_titles = [title.text for title in titles if title.text.strip() != '']

# Path to save the CSV file
csv_file_path = "/Volumes/scire/lib_python_data_analysis/data_analysis_portfolio/cargurus/car_titles.csv"

# Write data to CSV file
with open(csv_file_path, mode='w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(["Title"])  # Write header
    for title in car_titles:
        writer.writerow([title])

# Close the WebDriver
driver.quit()

if car_titles:
    print(f"Data successfully written to {csv_file_path}")
else:
    print("No car titles found.")
