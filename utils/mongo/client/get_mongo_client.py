from pymongo import MongoClient


def get_mongo_client(uri="mongodb://localhost:27017/", db_name="mydatabase"):
    """
    Helper function to get the MongoDB client and connect to a database.

    :param uri: MongoDB URI connection string
    :param db_name: Name of the database to connect to
    :return: Tuple of (client, database)
    """
    client = MongoClient(uri)
    db = client[db_name]
    return client, db
