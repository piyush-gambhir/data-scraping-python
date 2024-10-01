import json

def write_json(file_path, data):
    """
    Writes a Python dictionary or list to a JSON file.
    
    Args:
    file_path (str): The path to the JSON file.
    data (dict or list): The data to write to the JSON file.
    
    Returns:
    None
    """
    try:
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
    except Exception as e:
        print(f"Error writing JSON file {file_path}: {e}")
