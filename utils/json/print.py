import json

def pretty_print_json(file_path):
    """
    Reads and pretty-prints the JSON file content.
    
    Args:
    file_path (str): The path to the JSON file.
    
    Returns:
    None
    """
    try:
        data = read_json(file_path)
        if data is not None:
            print(json.dumps(data, indent=4, ensure_ascii=False))
    except Exception as e:
        print(f"Error pretty-printing JSON file {file_path}: {e}")
