from client import create_sqs_client

def send_message_to_sqs(queue_url, message_body, delay_seconds=0):
    """Send a message to an SQS queue"""
    sqs_client = create_sqs_client()
    if sqs_client is None:
        return False

    try:
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            DelaySeconds=delay_seconds
        )
        return response
    except Exception as e:
        print(f"An error occurred: {e}")
        return False
