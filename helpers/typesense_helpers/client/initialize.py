import os
from typesense import Client

from dotenv import load_dotenv
load_dotenv()


def initialize_typesense_client():
    client = Client({
        'api_key': os.getenv('TYPESENSE_API_KEY'),
        'nodes': [{
            'host': os.getenv('TYPESENSE_HOST'),
            'port': os.getenv('TYPESENSE_PORT'),
            'protocol': os.getenv('TYPESENSE_PROTOCOL')
        }],
        'connection_timeout_seconds': 2
    })
    return client
