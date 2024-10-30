import json


def read_json(file_path):
    """
    Reads a JSON file and returns its content.

    Args:
    file_path (str): The path to the JSON file.

    Returns:
    dict or list: The content of the JSON file as a dictionary or list.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as json_file:
            data = json.load(json_file)
        return data
    except Exception as e:
        print(f"Error reading JSON file {file_path}: {e}")
        return None
