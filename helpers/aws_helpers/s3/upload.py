# upload_file.py

from client import create_s3_client

def upload_file_to_s3(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket"""
    s3_client = create_s3_client()
    if s3_client is None:
        return False

    if object_name is None:
        object_name = file_name

    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
