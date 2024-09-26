import pandas as pd


def csv_to_json(file_path, json_path):
    """
    Converts a CSV file to a JSON file.

    Args:
    file_path (str): The path to the CSV file.
    json_path (str): The path where the JSON file will be saved.

    Returns:
    None
    """
    try:
        df = pd.read_csv(file_path)
        df.to_json(json_path, orient='records', indent=4)
    except Exception as e:
        print(f"Error converting CSV to JSON: {e}")


def json_to_csv(file_path, csv_path):
    """
    Converts a JSON file to a CSV file.

    Args:
    file_path (str): The path to the JSON file.
    csv_path (str): The path where the CSV file will be saved.

    Returns:
    None
    """
    try:
        df = pd.read_json(file_path)
        df.to_csv(csv_path, index=False)
    except Exception as e:
        print(f"Error converting JSON to CSV: {e}")
