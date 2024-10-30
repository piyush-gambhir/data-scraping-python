from utils.logger.setup import setup_logger
logger = setup_logger(__name__)


def capture_message(client, message: str, level: str = 'info'):
    """
    Capture a custom log message in APM.

    Args:
        client (Client): Elastic APM client instance.
        message (str): Custom message to log.
        level (str): Logging level for the message (default: 'info').
    """
    if client:
        try:
            logger.log(getattr(logging, level.upper(), 'info'),
                       f"Capturing message: {message}")
            client.capture_message(message)
        except Exception as e:
            logger.error(f"Error capturing message: {e}")
