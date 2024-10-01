def search_documents(client, collection_name: str, search_params: dict) -> dict:
    """
    Search documents in a Typesense collection.

    Args:
    - client: The Typesense client instance.
    - collection_name: The name of the collection to search in.
    - search_params: The search parameters as a dictionary.

    Returns:
    - dict: The search results.
    """
    try:
        return client.collections[collection_name].documents.search(search_params)
    except Exception as e:
        return {"error": f"Failed to search in collection '{collection_name}': {str(e)}"}
