from pymongo import MongoClient

def create_index(collection, field, order=1):
    """Create an index on the given field."""
    return collection.create_index([(field, order)])

def list_indexes(collection):
    """List all indexes in the collection."""
    return list(collection.list_indexes())

def drop_index(collection, index_name):
    """Drop an index by name."""
    collection.drop_index(index_name)

def drop_all_indexes(collection):
    """Drop all indexes in the collection."""
    collection.drop_indexes()
