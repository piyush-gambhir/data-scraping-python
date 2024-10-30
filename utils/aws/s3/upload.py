from utils.aws.s3.client import create_s3_client
from utils.logger.setup import setup_logger

logger = setup_logger(__name__)


def upload_file_to_s3(file_name, file_path, bucket, object_name=None):
    """
    Upload a file to an S3 bucket.

    :param file_name: The name of the file to upload.
    :param file_path: The full path to the file on the local system.
    :param bucket: The name of the S3 bucket.
    :param object_name: Optional. If not specified, file_name will be used as the object name.
    :return: The URL of the uploaded file if successful, else None.
    """
    s3_client = create_s3_client()
    if not s3_client:
        logger.error("Failed to initialize S3 client.")
        return None

    # Use file_name as object_name if none provided
    object_name = object_name or file_name

    try:
        logger.info(f"Starting upload of '{file_name}' from '{file_path}' to bucket '{bucket}' as '{object_name}'")
        s3_client.upload_file(file_path, bucket, object_name)
        logger.info(f"File '{file_name}' uploaded successfully to '{bucket}/{object_name}'")

        # Generate the URL of the uploaded file
        region = s3_client.meta.region_name
        url = f"https://{bucket}.s3.{region}.amazonaws.com/{object_name}"
        return url
    except FileNotFoundError as fnf_error:
        logger.error(f"File not found: {file_path}. Error: {fnf_error}")
    except Exception as e:
        logger.error(f"Error occurred while uploading '{file_name}' to S3: {e}")

    return None
