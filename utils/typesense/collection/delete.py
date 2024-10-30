def delete_collection(client, collection_name: str) -> dict:
    """
    Delete an existing collection from Typesense.

    Args:
    - client: The Typesense client instance.
    - collection_name: The name of the collection to delete.

    Returns:
    - dict: The deletion response.
    """
    try:
        return client.collections[collection_name].delete()
    except Exception as e:
        return {"error": f"Failed to delete collection '{collection_name}': {str(e)}"}