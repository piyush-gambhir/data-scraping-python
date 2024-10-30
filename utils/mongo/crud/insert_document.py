
def insert_document(collection, document):
    """
    Inserts a single document into the specified collection.
    
    :param collection: MongoDB collection object
    :param document: Dictionary representing the document to insert
    :return: Inserted document ID
    """
    insert_result = collection.insert_one(document)
    return insert_result.inserted_id
