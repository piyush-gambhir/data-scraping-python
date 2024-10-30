
from client import create_s3_client

def list_files_in_bucket(bucket):
    """List files in an S3 bucket"""
    s3_client = create_s3_client()
    if s3_client is None:
        return None

    try:
        response = s3_client.list_objects_v2(Bucket=bucket)
        return [item['Key'] for item in response.get('Contents', [])]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
