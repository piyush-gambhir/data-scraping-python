from typesense_helpers.client.initialize import initialize_typesense_client
from typesense_helpers.collection.export import export_typesense_collection


client = initialize_typesense_client()

# Specify the collection name and the output file
collection_name = 'movies'  # Replace with your collection name
output_filename = 'exported_data.json'

# Call the function to export the collection data
export_typesense_collection(client, collection_name, output_filename)
