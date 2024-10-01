def find_document(collection, query):
    """
    Find a single document that matches the query in the collection.
    
    :param collection: MongoDB collection object
    :param query: Dictionary representing the query filter
    :return: The found document or None
    """
    return collection.find_one(query)

def find_all_documents(collection, query=None):
    """
    Find all documents that match the query in the collection. If no query is provided, all documents are returned.
    
    :param collection: MongoDB collection object
    :param query: Dictionary representing the query filter (optional)
    :return: Cursor to the documents found
    """
    if query is None:
        query = {}
    return collection.find(query)
