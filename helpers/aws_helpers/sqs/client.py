import boto3
from botocore.exceptions import NoCredentialsError

def create_sqs_client():
    """Create an SQS client using boto3"""
    try:
        sqs_client = boto3.client('sqs')
        return sqs_client
    except NoCredentialsError:
        print("Credentials not available")
        return None
