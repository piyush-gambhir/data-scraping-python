# s3_client.py

import boto3
from botocore.exceptions import NoCredentialsError

def create_s3_client():
    """Create an S3 client"""
    try:
        s3_client = boto3.client('s3')
        return s3_client
    except NoCredentialsError:
        print("Credentials not available")
        return None
