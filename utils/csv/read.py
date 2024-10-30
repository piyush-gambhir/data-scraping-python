import csv
import pandas as pd


def read_csv(file_path):
    """
    Reads a CSV file and returns a list of dictionaries, where each dictionary represents a row.

    Args:
    file_path (str): The path to the CSV file.

    Returns:
    list: A list of dictionaries with the CSV data.
    """
    data = []
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append(row)
    except Exception as e:
        print(f"Error reading CSV file {file_path}: {e}")
    return data


def read_csv_pandas(file_path):
    """
    Reads a CSV file into a Pandas DataFrame.

    Args:
    file_path (str): The path to the CSV file.

    Returns:
    DataFrame: A Pandas DataFrame containing the CSV data.
    """
    try:
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        print(f"Error reading CSV file with Pandas: {e}")
        return None
