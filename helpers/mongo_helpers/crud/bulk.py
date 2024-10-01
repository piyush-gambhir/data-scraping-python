from pymongo import InsertOne, UpdateOne, DeleteOne

def bulk_insert(collection, docs):
    """Bulk insert multiple documents."""
    operations = [InsertOne(doc) for doc in docs]
    return collection.bulk_write(operations)

def bulk_update(collection, updates):
    """Bulk update multiple documents. Expects a list of tuples (filter, update)."""
    operations = [UpdateOne(filter, update) for filter, update in updates]
    return collection.bulk_write(operations)

def bulk_delete(collection, filters):
    """Bulk delete multiple documents."""
    operations = [DeleteOne(filter) for filter in filters]
    return collection.bulk_write(operations)
