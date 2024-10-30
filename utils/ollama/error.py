# error_handling.py
import ollama

def handle_errors(model_name):
    try:
        return ollama.chat(model=model_name)
    except ollama.ResponseError as e:
        print(f"Error: {e.error}")
        if e.status_code == 404:
            print(f"Model '{model_name}' not found. Attempting to pull the model...")
            ollama.pull(model_name)
