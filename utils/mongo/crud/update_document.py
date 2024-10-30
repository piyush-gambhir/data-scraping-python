def update_document(collection, filter_query, update_data):
    """
    Updates a single document in the collection based on a filter query.
    
    :param collection: MongoDB collection object
    :param filter_query: Dictionary representing the filter for selecting the document
    :param update_data: Dictionary representing the fields to update
    :return: Matched count and modified count
    """
    update_result = collection.update_one(filter_query, {"$set": update_data})
    return update_result.matched_count, update_result.modified_count
