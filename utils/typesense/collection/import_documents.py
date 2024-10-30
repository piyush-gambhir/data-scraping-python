import json


def import_typesense_collection(client, collection_name, input_filename):
    """
    Imports documents from a specified JSON file into a Typesense collection.

    :param client: Typesense client instance
    :param collection_name: Name of the Typesense collection to import data into
    :param input_filename: File name to read the data from (e.g., 'data.json')
    """
    try:
        # Read the JSON file containing the documents
        with open(input_filename, 'r') as input_file:
            documents = json.load(input_file)

        # Import each document into the Typesense collection
        for document in documents:
            client.collections[collection_name].documents.create(document)

        print(f"Successfully imported {len(documents)} documents into '{collection_name}'")

    except Exception as e:
        print(f"Error importing documents into collection '{collection_name}': {e}")
