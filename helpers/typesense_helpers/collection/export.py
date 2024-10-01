import json


def export_typesense_collection(client, collection_name, output_filename='typesense_collection_exported_data'):
    """
    Exports all documents from a Typesense collection to a specified JSON file.

    :param collection_name: Name of the Typesense collection to export
    :param output_filename: File name to save the exported data (e.g., 'data.json')
    :param typesense_config: Dictionary containing Typesense connection configuration
    """
    try:
        # Export the entire collection using the export API
        response = client.collections[collection_name].documents.export()

        # Format the response into a valid JSON array
        formatted_response = f"[{response.replace('}\n{', '},{')}]"

        # Convert the formatted string into a Python list of dictionaries
        documents = json.loads(formatted_response)

        # Save the exported documents to the specified JSON file
        with open(output_filename, 'w') as output_file:
            json.dump(documents, output_file, indent=4)

        print(f"Successfully exported {
              len(documents)} documents to '{output_filename}'")

    except Exception as e:
        print(f"Error exporting documents from collection '{
              collection_name}': {e}")
