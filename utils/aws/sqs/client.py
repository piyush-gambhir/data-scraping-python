import boto3
import os
from botocore.exceptions import NoCredentialsError

from utils.logger.setup import setup_logger

logger = setup_logger(__name__)


def create_sqs_client():
    """Create an SQS client using boto3"""
    sqs_client = None
    try:
        logger.info("Creating SQS client")
        if os.getenv('ENVIRONMENT') == 'DEVELOPMENT':
            sqs_client = boto3.client('sqs',
                                      region_name=os.getenv("AWS_REGION"),
                                      aws_access_key_id=os.getenv(
                                          "AWS_ACCESS_KEY_ID"),
                                      aws_secret_access_key=os.getenv(
                                          "AWS_SECRET_ACCESS_KEY"),
                                      )
        else:
            sqs_client = boto3.client('sqs')
        logger.info("SQS client created successfully")
    except NoCredentialsError:
        logger.error("Credentials not available")
    finally:
        return sqs_client
