def index_document(client, collection_name: str, document: dict) -> dict:
    """
    Index a single document to a Typesense collection.

    Args:
    - client: The Typesense client instance.
    - collection_name: The name of the collection to index the document.
    - document: The document to be indexed as a dictionary.

    Returns:
    - dict: The indexed document response.
    """
    try:
        return client.collections[collection_name].documents.create(document)
    except Exception as e:
        return {"error": f"Failed to index document in collection '{collection_name}': {str(e)}"}


def index_documents_bulk(client, collection_name: str, documents: list) -> dict:
    """
    Index multiple documents to a Typesense collection in bulk.

    Args:
    - client: The Typesense client instance.
    - collection_name: The name of the collection to index the documents.
    - documents: A list of documents to be indexed.

    Returns:
    - dict: The indexed documents response.
    """
    try:
        return client.collections[collection_name].documents.import_(documents)
    except Exception as e:
        return {"error": f"Failed to bulk index documents in collection '{collection_name}': {str(e)}"}
