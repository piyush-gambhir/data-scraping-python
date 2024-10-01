# download_file.py

from s3_client import create_s3_client

def download_file_from_s3(bucket, object_name, file_name=None):
    """Download a file from an S3 bucket"""
    s3_client = create_s3_client()
    if s3_client is None:
        return False

    if file_name is None:
        file_name = object_name

    try:
        s3_client.download_file(bucket, object_name, file_name)
        return True
    except FileNotFoundError:
        print("The file was not found")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
