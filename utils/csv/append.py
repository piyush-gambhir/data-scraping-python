import os
import csv

from utils.logger.setup import setup_logger

logger = setup_logger(__name__)


def append_csv(file_path, data, fieldnames):
    """
    Appends a list of dictionaries to an existing CSV file.

    Args:
    file_path (str): The path to the CSV file.
    data (list): A list of dictionaries with the data to append.
    fieldnames (list): The column names for the CSV.

    Returns:
    None
    """
    try:
        with open(file_path, mode='a', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writerows(data)
        logger.info(f"Successfully appended data to CSV file: {file_path}")
    except Exception as e:
        logger.error(f"Error appending to CSV file {file_path}: {e}")


def append_or_create_csv(file_path, data, fieldnames):
    """
    Appends to an existing CSV file or creates a new one if it does not exist.

    Args:
    file_path (str): The path to the CSV file.
    data (list): A list of dictionaries with the data to write.
    fieldnames (list): The column names for the CSV.

    Returns:
    None
    """
    try:
        # Check if file exists, if not, create it and write the header
        file_exists = os.path.exists(file_path)

        with open(file_path, mode='a' if file_exists else 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()  # Write header if it's a new file
                logger.info(f"Created new CSV file: {file_path}")
            else:
                logger.info(f"Appending to existing CSV file: {file_path}")

            writer.writerows(data)
        logger.info(f"Successfully wrote data to CSV file: {file_path}")
    except Exception as e:
        logger.error(f"Error writing to CSV file {file_path}: {e}")


def append_csv_pandas(file_path, df):
    """
    Appends a Pandas DataFrame to an existing CSV file.

    Args:
    file_path (str): The path to the CSV file.
    df (DataFrame): The Pandas DataFrame to append.

    Returns:
    None
    """
    try:
        df.to_csv(file_path, mode='a', header=False, index=False)
        logger.info(
            f"Successfully appended DataFrame to CSV file: {file_path}")
    except Exception as e:
        logger.error(f"Error appending CSV file with Pandas: {e}")


def append_or_create_csv_pandas(file_path, df):
    """
    Appends a Pandas DataFrame to an existing CSV file, or creates a new one if it does not exist.

    Args:
    file_path (str): The path to the CSV file.
    df (DataFrame): The Pandas DataFrame to append.

    Returns:
    None
    """
    try:
        # Check if the CSV file exists
        file_exists = os.path.exists(file_path)

        # Append if file exists, else create a new one
        df.to_csv(file_path, mode='a' if file_exists else 'w',
                  header=not file_exists, index=False)

        if file_exists:
            logger.info(
                f"Successfully appended DataFrame to existing CSV file: {file_path}")
        else:
            logger.info(
                f"Successfully created new CSV file with DataFrame: {file_path}")
    except Exception as e:
        logger.error(
            f"Error appending to or creating CSV file with Pandas: {e}")
