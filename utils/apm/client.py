import os
from elasticapm import Client

from utils.logger.setup import setup_logger
logger = setup_logger(__name__)


def create_apm_client():
    """
    Create and return an Elastic APM client instance.
    """
    try:
        client = Client({
            'SERVICE_NAME': os.getenv('ELASTIC_APM_SERVICE_NAME', 'VDP-PAGE-SCRAPER'),
            'SERVER_URL': os.getenv('ELASTIC_APM_SERVER_URL', 'http://localhost:8200'),
            'SECRET_TOKEN': os.getenv('ELASTIC_APM_SECRET_TOKEN', ''),
            'ENVIRONMENT': os.getenv('ELASTIC_APM_ENVIRONMENT', 'PROD'),
            # Ignore healthcheck endpoints
            'TRANSACTIONS_IGNORE_URLS': ['healthcheck'],
        })
        logger.info("Elastic APM client initialized successfully")
        return client
    except Exception as e:
        logger.error(f"Failed to initialize Elastic APM client: {e}")
        return None
