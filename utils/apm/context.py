from utils.logger.setup import setup_logger
logger = setup_logger(__name__)


def add_custom_context(client, context_data: dict):
    """
    Add custom context data to the current APM transaction.

    Args:
        client (Client): Elastic APM client instance.
        context_data (dict): Dictionary containing custom context data.
    """
    if client:
        try:
            logger.info(f"Adding custom context: {context_data}")
            client.add_custom_context(context_data)
        except Exception as e:
            logger.error(f"Error adding custom context: {e}")
