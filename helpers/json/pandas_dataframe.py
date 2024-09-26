import pandas as pd
from .read import read_json


def json_to_dataframe(file_path):
    """
    Converts a JSON file to a Pandas DataFrame.

    Args:
    file_path (str): The path to the JSON file.

    Returns:
    DataFrame: A Pandas DataFrame containing the JSON data.
    """
    try:
        data = read_json(file_path)
        df = pd.DataFrame(data)
        return df
    except Exception as e:
        print(f"Error converting JSON to DataFrame: {e}")
        return None


def dataframe_to_json(df, file_path, orient='records'):
    """
    Converts a Pandas DataFrame to a JSON file.

    Args:
    df (DataFrame): The Pandas DataFrame to convert.
    file_path (str): The path where the JSON file will be saved.
    orient (str): The format of the JSON. Default is 'records'.

    Returns:
    None
    """
    try:
        df.to_json(file_path, orient=orient, indent=4)
    except Exception as e:
        print(f"Error converting DataFrame to JSON: {e}")
