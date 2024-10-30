# import random
# import json
# from concurrent.futures import ThreadPoolExecutor, as_completed

# # Import the initialize function for Typesense client
# from typesense_helpers.client.initialize import initialize_typesense_client

# # Initialize the Typesense client
# client = initialize_typesense_client()

# # Define the collection name
# collection_name = 'dealerVinSchema'  # Replace with your collection name
# # save the document ids in json


# # Load the document IDs from 'data.json'
# with open('data.json', 'r') as f:
#     document_ids = json.load(f)

# # Filter out IDs with the value "01"
# filtered_ids = [doc.replace("{\"id\":\"", "").replace("\"}", "") for doc in document_ids if "01" not in doc]

# # Function to update a single document with a JSON odometer object
# def update_document(document_id):
#     # Generate a random odometer value
#     odometer_value = random.randint(10000, 500000)  # Generate an integer value for the odometer

#     # # Create the JSON object for odometer
#     # odometer_json = {
#     #     "value": odometer_value,
#     #     "unit": "miles"
#     # }

#     # Update the document with the new odometer JSON object
#     try:
#         client.collections[collection_name].documents[document_id].update({
#             'odometer': f"{odometer_value} miles"
#         })
#         print(f"Updated document ID: {document_id} with odometer value: {odometer_value} miles")
#     except Exception as e:
#         print(f"Failed to update document ID: {document_id}. Error: {str(e)}")

# # Use ThreadPoolExecutor to run updates in parallel
# max_workers = 10  # Adjust this value based on your server's capacity
# with ThreadPoolExecutor(max_workers=max_workers) as executor:
#     # Submit update tasks for each document ID
#     futures = [executor.submit(update_document, document_id) for document_id in filtered_ids]

#     # Wait for all futures to complete
#     for future in as_completed(futures):
#         future.result()

