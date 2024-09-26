import os

from .read import read_json
from .write import write_json


def append_json(file_path, new_data):
    """
    Appends new data to an existing JSON file. If the file does not exist, creates it.

    Args:
    file_path (str): The path to the JSON file.
    new_data (dict or list): The data to append to the JSON file.

    Returns:
    None
    """
    try:
        # Check if the file exists
        if os.path.exists(file_path):
            data = read_json(file_path)
            # If reading fails or returns None, initialize empty data
            if data is None:
                data = [] if isinstance(new_data, list) else {}
        else:
            # Initialize an empty structure depending on the type of new_data
            data = [] if isinstance(new_data, list) else {}

        # Append or update data
        if isinstance(data, list) and isinstance(new_data, list):
            data.extend(new_data)  # If both are lists, extend the list
        elif isinstance(data, dict) and isinstance(new_data, dict):
            data.update(new_data)  # If both are dicts, update the dictionary
        else:
            print("Data types don't match between file and new_data.")
            return

        # Write updated data back to the file
        write_json(file_path, data)

    except Exception as e:
        print(f"Error appending data to JSON file {file_path}: {e}")
