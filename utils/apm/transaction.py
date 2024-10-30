from utils.logger.setup import setup_logger
logger = setup_logger(__name__)


def start_transaction(client, name: str, transaction_type: str = 'custom'):
    """
    Start a new APM transaction.

    Args:
        client (Client): Elastic APM client instance.
        name (str): Name of the transaction.
        transaction_type (str): Type of transaction (default: 'custom').
    """
    if client:
        try:
            logger.info(f"Starting transaction: {name}")
            client.begin_transaction(transaction_type)
        except Exception as e:
            logger.error(f"Error starting transaction: {e}")


def end_transaction(client, name: str, result: str = 'success'):
    """
    End the current APM transaction.

    Args:
        client (Client): Elastic APM client instance.
        name (str): Name of the transaction.
        result (str): Result of the transaction (default: 'success').
    """
    if client:
        try:
            logger.info(f"Ending transaction: {name}")
            client.end_transaction(name, result)
        except Exception as e:
            logger.error(f"Error ending transaction: {e}")
