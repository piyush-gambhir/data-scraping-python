def delete_document(collection, filter_query):
    """
    Deletes a single document from the collection based on a filter query.
    
    :param collection: MongoDB collection object
    :param filter_query: Dictionary representing the filter for selecting the document
    :return: Count of deleted documents
    """
    delete_result = collection.delete_one(filter_query)
    return delete_result.deleted_count
