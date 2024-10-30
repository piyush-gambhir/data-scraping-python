from utils.logger.setup import setup_logger
logger = setup_logger(__name__)



def capture_exception(client, error_message: str = None):
    """
    Capture an exception in Elastic APM.

    Args:
        client (Client): Elastic APM client instance.
        error_message (str): Custom error message to log (default: None).
    """
    if client:
        try:
            logger.error(f"Capturing exception: {error_message}")
            client.capture_exception()
        except Exception as e:
            logger.error(f"Error capturing exception: {e}")
