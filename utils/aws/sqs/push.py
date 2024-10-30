import json
from utils.aws.sqs.client import create_sqs_client
from utils.logger.setup import setup_logger

logger = setup_logger(__name__)


def push_message_to_sqs(
    queue_url,
    message_body,
    delay_seconds=0,
    message_group_id=None,
    message_deduplication_id=None,  
):
    """
    Send a message to an SQS queue.

    :param queue_url: The URL of the SQS queue.
    :param message_body: The message body to send to the queue.
    :param delay_seconds: Optional. Delay in seconds before the message is delivered (default is 0).
    :param message_group_id: Optional. Required for FIFO queues, defines the group of the message.
    :param message_deduplication_id: Optional. Required for FIFO queues, defines the deduplication ID of the message.
    :return: True if the message was sent successfully, False otherwise.
    """
    sqs_client = create_sqs_client()

    if not sqs_client:
        logger.error("Failed to create SQS client")
        return False

    try:
        # Serialize message_body if it's a dictionary
        if isinstance(message_body, dict):
            message_body = json.dumps(message_body)

        send_params = {
            "QueueUrl": queue_url,
            "MessageBody": message_body,
            "DelaySeconds": delay_seconds,
        }

        # If message_group_id is provided, it's a FIFO queue, add MessageGroupId
        if message_group_id:
            send_params["MessageGroupId"] = message_group_id

        if message_deduplication_id:
            send_params["MessageDeduplicationId"] = message_deduplication_id
        
        logger.info(
            f"Sending message to SQS queue '{queue_url}' with delay of {delay_seconds} seconds"
        )
        response = sqs_client.send_message(**send_params)
        logger.info(
            f"Message sent successfully. MessageId: {response.get('MessageId')}"
        )
        return True
    except Exception as e:
        logger.error(f"An error occurred while sending message to SQS: {e}")
        return False
