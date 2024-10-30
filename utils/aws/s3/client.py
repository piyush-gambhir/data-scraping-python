# s3_client.py
import os
import boto3
from botocore.exceptions import NoCredentialsError

from utils.logger.setup import setup_logger
logger = setup_logger(__name__)


def create_s3_client():
    """Create an S3 client"""
    s3_client = None
    try:
        logger.info("Creating S3 client")
        if os.getenv('ENVIRONMENT') == 'DEVELOPMENT':
            s3_client = boto3.client(
                's3',
                aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                region_name=os.getenv('REGION_NAME')
            )
        else:
            s3_client = boto3.client('s3')
        logger.info("S3 client created successfully")
    except NoCredentialsError:
        logger.error("AWS Credentials not available")
    finally:
        return s3_client
