from client import create_sqs_client

def receive_messages_from_sqs(queue_url, max_messages=1, wait_time_seconds=0):
    """Receive messages from an SQS queue"""
    sqs_client = create_sqs_client()
    if sqs_client is None:
        return None

    try:
        response = sqs_client.receive_message(
            QueueUrl=queue_url,
            MaxNumberOfMessages=max_messages,
            WaitTimeSeconds=wait_time_seconds,
            MessageAttributeNames=['All']
        )
        return response.get('Messages', [])
    except Exception as e:
        print(f"An error occurred: {e}")
        return None
