def search_collection(client, collection_name, search_parameters):
    return client.collections[collection_name].documents.search(search_parameters)
