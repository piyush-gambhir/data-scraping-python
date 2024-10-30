import csv
# import pandas as pd

from utils.logger.setup import setup_logger

logger = setup_logger(__name__)


def write_csv(file_path, data, fieldnames):
    """
    Writes a list of dictionaries to a CSV file.

    Args:
    file_path (str): The path to the CSV file.
    data (list): A list of dictionaries with the data to write.
    fieldnames (list): The column names for the CSV.

    Returns:
    None
    """
    try:
        logger.info(f"Writing CSV file to {file_path}")

        if not data:
            logger.warning("Data is empty. CSV file will be created with only headers.")
            # Write only the headers and return early
            with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
            return

        with open(file_path, mode="w", newline="", encoding="utf-8") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for row in data:
                filtered_row = {k: v for k, v in row.items() if k in fieldnames}
                writer.writerow(filtered_row)

        logger.info(f"CSV file written to {file_path}")
        logger.debug(f"Number of rows written: {len(data)}")

    except Exception as e:
        logger.error(f"Error writing CSV file {file_path}: {e}")
        raise  # Re-raise the exception for higher-level error handling


# def write_csv_pandas(file_path, df, include_index=False):
#     """
#     Writes a Pandas DataFrame to a CSV file.

#     Args:
#     file_path (str): The path to the CSV file.
#     df (DataFrame): The Pandas DataFrame to write.
#     include_index (bool): Whether to include the DataFrame's index as a column (default: False).

#     Returns:
#     None
#     """
#     try:
#         df.to_csv(file_path, index=include_index)
#     except Exception as e:
#         logger.error(f"Error writing CSV file with Pandas: {e}")
