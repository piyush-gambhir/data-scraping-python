import pandas as pd
import csv


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
        with open(file_path, mode='w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(data)
    except Exception as e:
        print(f"Error writing CSV file {file_path}: {e}")


def write_csv_pandas(file_path, df, include_index=False):
    """
    Writes a Pandas DataFrame to a CSV file.

    Args:
    file_path (str): The path to the CSV file.
    df (DataFrame): The Pandas DataFrame to write.
    include_index (bool): Whether to include the DataFrame's index as a column (default: False).

    Returns:
    None
    """
    try:
        df.to_csv(file_path, index=include_index)
    except Exception as e:
        print(f"Error writing CSV file with Pandas: {e}")
