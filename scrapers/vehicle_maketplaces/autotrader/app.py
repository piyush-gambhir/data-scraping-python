import xml.etree.ElementTree as ET
import json

def parse_sitemap(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Namespace used in the XML
    ns = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9',
          'image': 'http://www.google.com/schemas/sitemap-image/1.1'}

    # Dictionary to store the results
    vehicles_data = []
    vehicle_count = 0

    # Iterate over all <url> elements in the XML
    for url_elem in root.findall('ns:url', ns):
        vehicle_url = url_elem.find('ns:loc', ns).text
        image_urls = [img.find('image:loc', ns).text for img in url_elem.findall('image:image', ns)]
        
        # Create a dictionary entry for each vehicle URL and its associated image URLs
        vehicle_entry = {
            "vehicle_url": vehicle_url,
            "image_urls": image_urls
        }
        vehicles_data.append(vehicle_entry)
        vehicle_count += 1  # Increment vehicle count

    # Add the vehicle count to the data
    output_data = {
        "total_vehicles": vehicle_count,
        "vehicles": vehicles_data
    }

    # Convert the data to JSON format and save it to a file
    with open('vehicle_data.json', 'w') as json_file:
        json.dump(output_data, json_file, indent=4)

    print(f"Data has been extracted and saved to vehicle_data.json with a total of {vehicle_count} vehicles.")

# Provide the path to your XML file
xml_file = 'inventory.xml'
parse_sitemap(xml_file)
