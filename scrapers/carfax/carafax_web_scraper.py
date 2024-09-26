# Importing the libraries
from bs4 import BeautifulSoup
import pandas as pd
import csv
from datetime import datetime
import requests
import time

# # Open the HTML file in binary mode and decode it 
# with open('test.html', 'rb') as file:
#     html_content = file.read().decode('utf-8')

options = webdriver.ChromeOptions()

options.add_argument("--incognito")
options.add_experimental_option("useAutomationExtension", False)
options.add_experimental_option("excludeSwitches",["enable-automation"])
driver = webdriver.Chrome(options=options)
driver.execute_cdp_cmd('Network.setUserAgentOverride', {
                       "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.53 Safari/537.36'})
driver.get("https://www.carfax.com/VehicleHistory/ar20/bZPMRrM0iRB2ZV0SD_W_2aDgkIGHjGqYfHDvloZqte3l4hR0mLfkxHvfFJZshrUQ4IXnGgdqqYhQqI8DSy6AysCEMeojSuTQasw#ownership-history-section")
time.sleep(15)
quit()

cookies = {
    '70fdde380e': 'af820d3c90b6f47b756d7e35bf85683a',
    's247cname': 'bba932ab-6c4a-4250-84b8-b5a5c35287f0',
    'JSESSIONID': '5500CC87F1F48B6B4F3976ADC5178DAF',
    'httpReferrer1': 'https%3A%2F%2Fwww.google.com%2F',
    'landingPageUrl': 'https%3A%2F%2Fwww.site24x7.com%2Ftools%2Frestapi-tester.html',
    '3ed8788753': 'de8e823b16b09662718e53ad71a7454c',
    'site24x7-_zldt': '9bbccc62-0513-437e-85e2-13b48d19aa3f-2',
    'site24x7-_zldp': 'c0tmAe%2BHc72O0inLu%2BZUZ87WgDk%2B%2FOpkCSdpIcXSJykhI31%2FcKZiMhDj3qh1Vpdp61H4KQEA5qU%3D',
    'site24x7-_uuid': 'e1ae7550-23f4-44a3-882c-b1a4c273b68c_a116',
}

headers = {
    'Accept': '*/*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Cookie': '70fdde380e=af820d3c90b6f47b756d7e35bf85683a; s247cname=bba932ab-6c4a-4250-84b8-b5a5c35287f0; _zcsr_tmp=bba932ab-6c4a-4250-84b8-b5a5c35287f0; JSESSIONID=5500CC87F1F48B6B4F3976ADC5178DAF; httpReferrer1=https%3A%2F%2Fwww.google.com%2F; landingPageUrl=https%3A%2F%2Fwww.site24x7.com%2Ftools%2Frestapi-tester.html; 3ed8788753=de8e823b16b09662718e53ad71a7454c; site24x7-_zldt=9bbccc62-0513-437e-85e2-13b48d19aa3f-2; site24x7-_zldp=c0tmAe%2BHc72O0inLu%2BZUZ87WgDk%2B%2FOpkCSdpIcXSJykhI31%2FcKZiMhDj3qh1Vpdp61H4KQEA5qU%3D; site24x7-_uuid=e1ae7550-23f4-44a3-882c-b1a4c273b68c_a116',
    'Origin': 'https://www.site24x7.com',
    'Referer': 'https://www.site24x7.com/tools/restapi-tester.html',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
    'X-Requested-With': 'XMLHttpRequest',
    'sec-ch-ua': '"Not.A/Brand";v="8", "Chromium";v="114", "Google Chrome";v="114"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
}

data = 'method=G&url=https%3A%2F%2Fwww.carfax.com%2FVehicleHistory%2Far20%2FjKxdPDQjvl6AGjEh2_w37tvXkSG02NmMzsLf5OjmZntW4puHm86HTMbV06s9_LMM45XCej9TxDG_e96N5IlHGFrj2Ei3RbROkz8%23additional-history-section&headername=User-Agent&headervalue=Mozilla%2F5.0+(Macintosh%3B+Intel+Mac+OS+X+10_15_7)+AppleWebKit%2F537.36+(KHTML%2C+like+Gecko)+Chrome%2F86.0.4240.80+Safari%2F537.36&bodytype=T&locationid=33'

response = requests.post('https://www.site24x7.com/tools/restapi-tester',
                         cookies=cookies, headers=headers, data=data)

print(response.json())

quit()

# Create a BeautifulSoup object
soup = BeautifulSoup(html_content, 'html.parser')


"""
------------------ Extracting the CARFAX Report Details ------------------
"""

"""
Vehcile Details
"""

# Extracting the Vehicle Details
vehicle_details = soup.find('div', class_='vehicle-information')

# Find the vehicle information div
vehicle_info_div = soup.find('div', class_='vehicle-information')

# Extract the Vehicle Details
year_make_model = vehicle_info_div.find(
    'div', class_='vehicle-information-year-make-model').text.strip()
vin = vehicle_info_div.find_all('div')[1].find_all('span')[1].text.strip()
sedan_type = vehicle_info_div.find_all('div')[2].text.strip()
engine = vehicle_info_div.find_all('div')[3].text.strip()
fuel_type = vehicle_info_div.find_all('div')[4].text.strip()
drive_type = vehicle_info_div.find_all('div')[5].text.strip()

# Create a list of dictionaries for vehicle details
vehicle_data = [{'Attribute': 'Year Make Model', 'Details': year_make_model},
                {'Attribute': 'VIN', 'Details': vin},
                {'Attribute': 'Sedan Type', 'Details': sedan_type},
                {'Attribute': 'Engine', 'Details': engine},
                {'Attribute': 'Fuel Type', 'Details': fuel_type},
                {'Attribute': 'Drive Type', 'Details': drive_type}]


"""
Ownership History
"""

# Extracting the Ownership History
table = soup.find('table', id='ownership-history-section')
# Extract the table headers
headers = [th.text.strip() for th in table.select('thead th')]
# Extract the table rows
ownership_history_rows = []
for tr in table.select('tbody tr'):
    row = [td.text.strip() for td in tr.select('td')]
    ownership_history_rows.append(row)

ownership_history_rows[2] = [row.split('\n')[0]
                             for row in ownership_history_rows[2]]
ownership_history_rows[4] = [row.split('\n')[0]
                             for row in ownership_history_rows[4]]

# Add attribute names to headers
attribute_names = [div.text.strip() for div in table.select(
    '.common-section-row-heading div:nth-child(2)')]

headers = ['Attribute'] + headers
headers.pop(1)
for i in range(1, len(headers)):
    headers[i] = "Owner " + str(i)

# Add attribute names to each row
for i, row in enumerate(ownership_history_rows):
    row.insert(0, attribute_names[i])


"""
Additional History
"""

# Extracting the Additional History
table = soup.find('table', id='additional-history-section')

# Extract the table headers
headers = [th.text.strip() for th in table.select('thead th')]

# Extract the table rows
additional_history_rows = []
for tr in table.select('tbody tr'):
    row = [td.text.strip() for td in tr.select('td')]
    additional_history_rows.append(row)

# Add attribute names to headers
attribute_names = [div.text.strip() for div in table.select(
    '.common-section-row-heading div:nth-child(2)')]
headers = ['Attribute'] + headers
headers.pop(1)
for i in range(1, len(headers)):
    headers[i] = "Owner " + str(i)

# Add attribute names to each row
for i, row in enumerate(additional_history_rows):
    row.insert(0, attribute_names[i])

"""
CARFAX Logo Details
"""

# Extracting the CARFAX Logo Details
owner_blocks = soup.find_all('div', class_='owner-block')
owners_data = []

for owner_block in owner_blocks:
    owner_data = {}
    owner_data['purchase_year'] = owner_block.find(
        'div', class_='purchase-year').text.strip().split(':')[1].strip()
    owner_data['owner_type'] = owner_block.find(
        'div', class_='owner-type').text.strip()

    records = owner_block.find(
        'table', class_='detailed-history-records').find_all('tr', class_='detailed-history-row detailed-history-row-main')

    owner_records = []

    for record in records:
        # dictionary to store record data
        record_data = {}

        # Extract the record data
        # Date
        date = record.find_all(
            'td', class_='record-normal-first-column')[0].text.strip()[:10]
        record_data['date'] = date
        # Mileage
        mileage = record.find(
            'td', class_='record-odometer-reading').text.split(' ')
        mileage = mileage[0].strip() + ' ' + mileage[-1].strip()
        record_data['mileage'] = mileage
        # Source
        source = record.find(
            'td', class_='record-source').find('p', class_='detail-record-source-line').text.split('\n')
        source = joined_string = ' '.join(map(lambda x: x.strip(), source))
        record_data['source'] = source
        # Comments
        comments = []
        record_comments = record.find(
            'td', class_='record-comments')
        comments_list = record_comments.find_all(
            'li', class_='record-comments-group-inner-line')
        for comment in comments_list:
            comment = comment.text.split("\n")
            comment = ' '.join(map(lambda x: x.strip(), comment))
            comments.append(comment)

        comments = result = ', '.join(comment.strip() for comment in comments)
        record_data['comments'] = comments
        owner_records.append(record_data)

    owner_data['records'] = owner_records
    owners_data.append(owner_data)

"""
------------------ Saving Data to CSV ------------------
"""

output_folder_path = "CARFAX_data"

# Create a DataFrame for vehicle details
vehicle_df = pd.DataFrame(vehicle_data)

# Create a DataFrame for ownership details
ownership_df = pd.DataFrame(ownership_history_rows, columns=headers)

# Create a DataFrame for additional history details
additional_df = pd.DataFrame(additional_history_rows, columns=headers)


# Save data to CSV with different sections
output_filename = 'CARFAX_report.csv'
with open(output_filename, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)

    # Write vehicle details section
    writer.writerow(['Vehicle Details'])
    writer.writerow(['Attribute', 'Details'])
    for _, row in vehicle_df.iterrows():
        writer.writerow(row)

    # Add spacing between sections
    writer.writerow([])

    # Write ownership details section
    writer.writerow(['Ownership Details'])
    writer.writerow(headers)
    for _, row in ownership_df.iterrows():
        writer.writerow(row)

    # Add spacing between sections
    writer.writerow([])

    # Write additional history section
    writer.writerow(['Additional History'])
    writer.writerow(headers)
    for _, row in additional_df.iterrows():
        writer.writerow(row)

    # Add spacing between sections
    writer.writerow([])

    # Write CARFAX logo details section
    writer.writerow(['CARFAX Logo Details'])

    for i in range(len(owners_data)):
        writer.writerow(['Owner ' + str(i+1)])
        writer.writerow(['Purchase Year', owners_data[i]['purchase_year']])
        writer.writerow(['Owner Type', owners_data[i]['owner_type']])
        writer.writerow(['Date', 'Mileage', 'Source', 'Comments'])
        for record in owners_data[i]['records']:
            date = datetime.strptime(record['date'], '%m/%d/%Y')
            formatted_date = datetime.strftime(date, '%Y-%m-%d')
            writer.writerow([formatted_date, record['mileage'],
                            record['source'], record['comments']])
        writer.writerow([])
