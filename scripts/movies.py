from typesense import Client
import json

# Initialize the Typesense client


def initialize_typesense_client():
    return Client({
        'nodes': [{
            'host': 'localhost',  # Replace with your Typesense host
            'port': '8108',       # Replace with your Typesense port
            'protocol': 'http'    # Replace with the protocol if different
        }],
        'api_key': 'xyz',          # Replace with your Typesense API key
        'connection_timeout_seconds': 300
    })

# Create the collection


def create_typesense_collection(client, collection_name, schema):
    # Check if the collection exists
    try:
        client.collections[collection_name].retrieve()
        print(f"Collection '{collection_name}' already exists.")
    except Exception as e:
        print(f"Collection '{
              collection_name}' does not exist. Creating a new collection.")
        # If collection does not exist, create it
        client.collections.create(schema)
        print(f"Collection '{collection_name}' created successfully.")

# Import data into the collection


def import_typesense_collection(client, collection_name, data_filename):
    with open(data_filename, 'r') as f:
        data = json.load(f)
    for document in data:
        try:
            client.collections['movies'].documents.import_(
                data, {'action': 'create'})
        except Exception as e:
            print(f"Failed to import document ID {document['id']}: {e}")


# Define the schema (fixed)
collection_schema = {
    "name": "movies",
    "fields": [
        {"name": "id", "type": "string"},
        {"name": "imdbId", "type": "string", "facet": False},
        {"name": "title", "type": "string", "facet": False},
        {"name": "originalTitle", "type": "string", "facet": False},
        {"name": "backdropPath", "type": "string", "optional": True},
        {"name": "posterPath", "type": "string", "optional": True},
        {"name": "overview", "type": "string", "facet": False, "optional": True},
        {"name": "releaseDate", "type": "string",
            "facet": False, "optional": True},
        # Remove "optional" from this field
        {"name": "popularity", "type": "float", "facet": False},
        {"name": "adult", "type": "bool", "facet": True, "optional": True},
        {"name": "mediaType", "type": "string", "facet": True, "optional": True},
        {"name": "genres", "type": "string[]", "facet": True, "optional": True},
        {"name": "originalLanguage", "type": "string",
            "facet": True, "optional": True},
        {"name": "voteAverage", "type": "float", "facet": True, "optional": True},
        {"name": "voteCount", "type": "int32", "facet": False, "optional": True},
        {"name": "createdAt", "type": "string", "optional": True},
        {"name": "updatedAt", "type": "string", "optional": True}
    ],
    "default_sorting_field": "popularity"  # Default sorting field must be required
}

# Initialize the client
client = initialize_typesense_client()

# Collection name
collection_name = 'movies'

# Specify the filename for the data to be imported
data_filename = 'exported_data.json'  # Replace with your data file path

# Step 1: Create the collection
create_typesense_collection(client, collection_name, collection_schema)

# Step 2: Import the collection data
import_typesense_collection(client, collection_name, data_filename)
