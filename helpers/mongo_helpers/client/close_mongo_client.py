def close_mongo_client(client):
    """
    Helper function to close the MongoDB client connection.

    :param client: MongoClient object
    """
    client.close()
    print("MongoDB connection closed.")
